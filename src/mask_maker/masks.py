import dataclasses
from gerbonara import LayerStack
from gerbonara import graphics_object as go
from gerbonara.utils import Tag , MM , sum_bounds
import warnings

def get_board_bounds(stack: LayerStack , units = MM):
    outline = stack.outline
    if outline is None:
        warnings.warn("No outline found, defaulting to board_bounds, which may be inaccurate.")
        return stack.board_bounds(unit = units)

    boxes = []
    for obj in outline.instance.objects:
        if isinstance(obj , (go.Line , go.Arc)):
            prim = obj.as_primitive(units)
            boxes.append(dataclasses.replace(prim, width=0).bounding_box())
        elif isinstance(obj , go.Region):
            boxes.append(obj.bounding_box(units))
        else:
            continue

    if not boxes:
        warnings.warn("Outline did not contain Lines, Arcs, or Regions. Defaulting to board_bounds, which may be inaccurate.")
        return stack.board_bounds(unit = units)

    return sum_bounds(boxes)

    


def masks_from_stack(stack: LayerStack , job: dict) -> dict[str , Tag]:
    bounds = get_board_bounds(stack)
    masks = {}
    job_masks = list(job.values())
    for mask_name , mask_properties in job_masks:
        if mask_properties["type"] == "folded":
            masks[mask_name] = folded_mask_from
