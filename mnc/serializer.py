from datetime import date

class serialize_data:
    @staticmethod
    def serial_data(data):
        if isinstance(data, list):
            return [serialize_data.serial_data(item) for item in data]
        elif isinstance(data, dict):
            return {key: serialize_data.serial_data(value) for key, value in data.items()}
        elif isinstance(data, date):
            return data.isoformat()  
        return data
