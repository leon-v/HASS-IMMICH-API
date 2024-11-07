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
        self.entitiesCreadted = False

    def getEntities(self) -> List[Entity]:

        if self.entitiesCreadted:
            return self.entities

        self.entities.extend(self.buildEntities('Thumbnail Generation', 'thumbnailGeneration'))
        self.entities.extend(self.buildEntities('Metadata Extraction', 'metadataExtraction'))
        self.entities.extend(self.buildEntities('Video Conversion', 'videoConversion'))
        self.entities.extend(self.buildEntities('Face Detect', 'faceDetection'))
        self.entities.extend(self.buildEntities('Face Recognition', 'facialRecognition'))
        self.entities.extend(self.buildEntities('Smart Search', 'smartSearch'))
        self.entities.extend(self.buildEntities('Duplicate Detection', 'duplicateDetection'))
        self.entities.extend(self.buildEntities('Storage Template Migration', 'storageTemplateMigration'))
        self.entities.extend(self.buildEntities('Migration', 'migration'))
        self.entities.extend(self.buildEntities('Search', 'search'))
        self.entities.extend(self.buildEntities('Sidecar', 'sidecar'))
        self.entities.extend(self.buildEntities('Library', 'library'))
        self.entities.extend(self.buildEntities('Notifications', 'notifications'))
        self.entities.extend(self.buildEntities('Backup Database', 'backupDatabase'))

        return self.entities

    def buildEntities(self, name: str, property: str) -> List[Entity]:
        entities = []

        entities.append(QueueSizeNumberEntity(
            self,
            [property, 'jobCounts' ,'active'],
            f"- {name}",
            '- Active'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            [property, 'jobCounts' ,'failed'],
            f"- {name}",
            '- Failed'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            [property, 'jobCounts' ,'waiting'],
            f"- {name}",
            '- Waiting'
        ))

        entities.append(QueueSizeNumberEntity(
            self,
            [property, 'jobCounts' ,'paused'],
            f"- {name}",
            '- Paused'
        ))

        entities.append(QueueStatusBoolEntity(
            self,
            [property, 'queueStatus', 'isActive'],
            f"- {name}",
            '- Active'
        ))

        metadataExtractionCommandRequest = RestRequest(hub = self.hub, method = "PUT", uriPath = f"/api/jobs/{property}")
        entities.append(QueuePauseResumeSwitch(
            self,
            [property, 'queueStatus', 'isPaused'],
            f"- {name}",
            '- Paused',
            onCommand = RestCommand(metadataExtractionCommandRequest, {"command": "pause", "force": False}),
            offCommand = RestCommand(metadataExtractionCommandRequest, {"command": "resume", "force": False}),
            responsePath = ['queueStatus', 'isPaused'],
        ))

        return entities
