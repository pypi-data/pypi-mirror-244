from dataclasses import dataclass

from sigma.exceptions import SigmaTransformationError
from sigma.processing.pipeline import ProcessingPipeline, ProcessingItem
from sigma.processing.transformations import DetectionItemFailureTransformation
from sigma.rule import SigmaDetectionItem


@dataclass
class FieldMappingFailureTransformation(DetectionItemFailureTransformation):
    """
    Raise a SigmaTransformationError with the provided message for unsupported fields.
    The supported field can be found on 'QRadarAQL.sigma.mapping.fields' and
    'QRadarKQL.sigma.mapping.fields'
    """
    message: str
    qradar_field_mapping: dict

    def apply_detection_item(self, detection_item: SigmaDetectionItem) -> None:
        field = detection_item.field
        if field not in self.qradar_field_mapping:
            raise SigmaTransformationError(self.message.format(field=field))


def QRadar_fields_pipeline(base_pipeline_items, field_mapping) -> ProcessingPipeline:
    """
    Pipeline supporting only fields that can be mapped
    """
    processing_pipeline = ProcessingPipeline(
        name="Qradar fields",
        priority=20,
        items=[
                  ProcessingItem(
                      identifier="QRadar_unsupported_fields",
                      transformation=FieldMappingFailureTransformation(
                          message="field '{field}' is not supported",
                          qradar_field_mapping=field_mapping
                      ),
                  ),
              ] + base_pipeline_items
    )
    return processing_pipeline
