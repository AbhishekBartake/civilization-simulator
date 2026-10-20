import random
from civilisation_model import Civilisation
from simulation import Simulation


if __name__ == "__main__":
    while True:
        student_id = input("Enter your 9-digit student ID: ").strip()

        if Civilisation.is_valid_student_id(student_id):
            break

        print("Invalid ID. Please enter exactly 9 digits.")

    random.seed(int(student_id))


    try:
        simulation = Simulation(student_id)
    except RuntimeError as error:
        print(error)
    else:
        simulation.run()
