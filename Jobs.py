from typing import List

from homeassistant.helpers.entity import Entity

from .Hub  import Hub
from .RestEndpoint import RestEndpoint
from .RestRequest import RestRequest
from .RestCommand import RestCommand
from .QueueSizeNumberEntity import QueueSizeNumberEntity
from .QueueStatusBoolEntity import QueueStatusBoolEntity
from .QueuePauseResumeSwitch import QueuePauseResumeSwitch

class Jobs(RestEndpoint):
    def __init__(self, hub: Hub):
        super().__init__(hub, 'jobs', 'Jobs')
        self.entities = []

    def getEntities(self) -> List[Entity]:
        entities = []

        entities.append(QueueSizeNumberEntity(
            self,
            ['thumbnailGeneration', 'jobCounts' ,'active'],
            '- Thumbnails',
            '- Active'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            ['thumbnailGeneration', 'jobCounts' ,'failed'],
            '- Thumbnail',
            '- Failed'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            ['thumbnailGeneration', 'jobCounts' ,'waiting'],
            '- Thumbnail',
            '- Waiting'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            ['thumbnailGeneration', 'jobCounts' ,'paused'],
            '- Thumbnail',
            '- Paused'
        ))

        entities.append(QueueStatusBoolEntity(
            self,
            ['thumbnailGeneration', 'queueStatus', 'isActive'],
            '- Thumbnails',
            '- Active'
        ))

        thumbnailGenerationCommandRequest = RestRequest(hub = self.hub, method = "PUT", uriPath = "/api/jobs/thumbnailGeneration")
        entities.append(QueuePauseResumeSwitch(
            self,
            ['thumbnailGeneration', 'queueStatus', 'isPaused'],
            '- Thumbnails',
            '- Is Paused',
            onCommand = RestCommand(thumbnailGenerationCommandRequest, {"command": "pause", "force": False}),
            offCommand = RestCommand(thumbnailGenerationCommandRequest, {"command": "resume", "force": False}),
            responsePath = ['queueStatus', 'isPaused'],
        ))

        return entities