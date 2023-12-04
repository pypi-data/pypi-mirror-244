import json
from collections import defaultdict
from typing import Union

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest

from . import blocks, exceptions
from .logging import logger
from .processors import BaseProcessor
from .typing import BlockInstance, TemplateContext


def get_block_output(
    processor: BaseProcessor,
    block: BlockInstance,
    context: TemplateContext,
    request: WSGIRequest = None
):
    try:
        return processor.render(block, context, request=request)
    except exceptions.SkipBlock:
        return ""


def render_stream(
    stream: Union[str, list],
    context: TemplateContext = None,
    request: WSGIRequest = None
) -> str:
    """
    Render all content blocks contained in the provided JSON array.

    This function processes each content block within the JSON array
    and renders them into a single HTML string. You can provide
    an optional context to include additional data in the rendering process.
    """
    if isinstance(stream, str):
        stream = json.loads(stream)

    if not isinstance(stream, list):
        raise exceptions.InvalidStreamTypeError(stream)

    # Phase 1: Filter out invisible blocks, fill `per_model_ids` map.
    per_model_ids = defaultdict(list)
    filtered_stream = []
    for record in stream:
        if not blocks.is_valid(record):
            raise exceptions.InvalidStreamBlockError(record)

        visible = record.get("visible", True)
        if not visible:
            continue

        try:
            model = blocks.get_model(record)
        except LookupError:
            logger.warning("Invalid block: %r", record)
            continue

        per_model_ids[model].append(record["pk"])
        filtered_stream.append(record)

    # Phase 2: Fetch the data for blocks.
    model_processors = {}
    per_model_blocks = {}
    for model, ids in per_model_ids.items():
        processor = blocks.get_processor(model)
        model_processors[model] = processor

        queryset = processor.get_queryset()
        per_model_blocks[model] = queryset.in_bulk(ids)

    # Phase 3: Render each block.
    output = []
    for record in filtered_stream:
        model = blocks.get_model(record)

        pk = model._meta.pk.get_prep_value(record["pk"])
        block_instance = per_model_blocks[model].get(pk)
        if block_instance is None:
            logger.warning("Block does not exist: %r", record)
            continue

        processor = model_processors[model]
        block_output = get_block_output(processor, block_instance, context, request)
        if block_output:
            output.append(block_output)

    return "\n".join(output)


def render_block(
    record: dict,
    context: TemplateContext = None,
    request: WSGIRequest = None
):
    """
    Helper method not used by the library because rendering
    each block separately leads to unnecessary SQL queries.
    """
    try:
        model = blocks.get_model(record)
    except LookupError:
        logger.warning("Invalid block: %r", record)
        return

    processor = blocks.get_processor(model)
    queryset = processor.get_queryset()
    pk = model._meta.pk.get_prep_value(record["pk"])

    try:
        block = queryset.get(pk=pk)
    except (KeyError, ObjectDoesNotExist, MultipleObjectsReturned):
        logger.warning("Invalid block: %r", record)
    else:
        return get_block_output(processor, block, context, request)
