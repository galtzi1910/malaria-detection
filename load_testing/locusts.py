from locust import SequentialTaskSet, HttpUser, task


class DetectorTask(SequentialTaskSet):
    @task
    def detection(self):
        with open(
            "../data/downloads/extracted/ZIP.data.lhnc.nlm.nih.gov_publ_Mala_cell_imagCpSVVrJBQVm1EAGSYJgFN2ZUxCZtjRh76bGSL61Dxmg.zip/cell_images/Parasitized/C33P1thinF_IMG_20150619_114756a_cell_179.png",
            "rb",
        ) as image:
            self.client.post("/uploadFile", files={"im": image})


class LoadTester(HttpUser):
    host = "http://localhost:8000"
    tasks = [DetectorTask]
