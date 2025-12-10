from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger(__name__)

BOOTSTRAP_SERVICES = ['broker:9092', 'broker:9093', 'broker:9094']


class KafkaProducerService:
    def __init__(self, topic_name: str):
        self.topic_name = topic_name
        self.producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVICES,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, data: dict):
        """Отправляет сообщение в настроенный топик."""
        try:
            logger.debug("kafka called")
            future = self.producer.send(self.topic_name, value=data)
            logger.info(
                f"Сообщение {future} отправлено в топик {self.topic_name}"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Kafka: {e}")
            raise


kafka_producer_instance: KafkaProducerService = None
