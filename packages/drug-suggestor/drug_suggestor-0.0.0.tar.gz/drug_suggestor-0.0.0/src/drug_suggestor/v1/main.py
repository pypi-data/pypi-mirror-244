"""
Main module for the drug suggestor.
"""

from typing import List

from .models import Company, Drug, Patient, Symptom


class DrugSuggestor:
    """
    Class for the drug suggestor.
    """

    def __init__(self, patient: Patient, symptoms: List[Symptom]):
        self.patient = patient
        self._symptoms = symptoms

    # setter and getter for symptoms

    @property
    def symptoms(self):
        return self._symptoms

    def suggest(self) -> List[Drug]:
        """
        Suggests a drug based on the patient's symptoms.
        """
        drugs = [
            Drug(
                name="Paracetamol",
                description="Paracetamol is a drug used to treat pain and fever. It is typically used for mild to moderate pain relief.",
                side_effects="Side effects include nausea and vomiting, but these are rare.",
                contraindications="Contraindications include liver disease, kidney disease, and alcoholism.",
                dosage="Dosage is 500mg every 4 hours.",
                manufacturer=[
                    Company(
                        name="Johnson & Johnson",
                        description="Johnson & Johnson is an American multinational corporation founded in 1886 that develops medical devices, \
                    pharmaceutical, and consumer packaged goods.",
                    )
                ],
            )
        ]
        return drugs
