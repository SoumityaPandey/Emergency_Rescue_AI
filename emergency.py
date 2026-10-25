import heapq
from datetime import datetime


class EmergencyManager:

    def __init__(self):
        self.queue = []
        self.emergencies = {}
        self.counter = 0

    def report_emergency(
        self,
        location,
        emergency_type,
        severity,
        description=""
    ):

        self.counter += 1

        emergency_id = f"EMG-{self.counter:03d}"

        report = {
            "id": emergency_id,
            "location": location,
            "type": emergency_type,
            "severity": severity,
            "status": "Reported",
            "reported_at": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),
            "description": description,
            "route": [],
            "rescue_center": None
        }

        self.emergencies[emergency_id] = report

        priority = {
            "Critical": 1,
            "High": 2,
            "Medium": 3,
            "Low": 4
        }.get(severity, 4)

        heapq.heappush(
            self.queue,
            (
                priority,
                self.counter,
                emergency_id
            )
        )

        return emergency_id

    def get_next_emergency(self):

        while self.queue:

            _, _, emergency_id = self.queue[0]

            report = self.emergencies.get(
                emergency_id
            )

            if (
                report
                and report["status"] == "Reported"
            ):
                return report

            heapq.heappop(self.queue)

        return None

    def assign_emergency(
        self,
        emergency_id,
        route,
        rescue_center
    ):

        if emergency_id not in self.emergencies:
            return False

        report = self.emergencies[emergency_id]

        report["route"] = route
        report["rescue_center"] = rescue_center
        report["status"] = "Assigned"

        return True

    def update_status(
        self,
        emergency_id,
        status
    ):

        if emergency_id not in self.emergencies:
            return False

        self.emergencies[emergency_id][
            "status"
        ] = status

        return True

    def get_all_emergencies(self):

        return list(
            self.emergencies.values()
        )