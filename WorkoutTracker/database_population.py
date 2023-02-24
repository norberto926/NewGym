from .models import Exercise, Equipment, Muscle, Set, WorkoutExercise, Workout, WorkoutTemplate


def populate_exercises_on_registration(request):

    #Equipment
    leg_press_machine = Equipment.objects.get(name='Leg Press machine')
    hammer_chest_machine = Equipment.objects.get(name='Hammer Chest machine')
    smith_machine = Equipment.objects.get(name='Smith machine')
    fly_machine = Equipment.objects.get(name='Fly machine')
    dip_pull_up_machine = Equipment.objects.get(name='Dip/Pull-up machine')
    tricep_dip_bar = Equipment.objects.get(name='Tricep Dip bar')
    exercise_atlas = Equipment.objects.get(name='Exercise Atlas')
    pull_up_bar = Equipment.objects.get(name='Pull-up bar')
    barbell = Equipment.objects.get(name='Barbell')
    dumbells = Equipment.objects.get(name='Dumbells')
    bench = Equipment.objects.get(name='Bench')
    load = Equipment.objects.get(name='Load (more than bodyweight)')

    #Chest exercises
    chest = Muscle.objects.get(name="Chest")
    push_ups = Exercise.objects.create(name='Push-up', owner=request.user, main_muscle_group=chest)
    machine_chest_flies = Exercise.objects.create(name='Machine chest flies', owner=request.user, main_muscle_group=chest)
    machine_chest_flies.equipment_needed.add(fly_machine)
    dumbell_chest_flies = Exercise.objects.create(name='Dumbell chest flies', owner=request.user, main_muscle_group=chest)
    dumbell_chest_flies.equipment_needed.add(bench)
    dumbell_chest_flies.equipment_needed.add(dumbells)
    cable_crossovers = Exercise.objects.create(name='Cable crossovers', owner=request.user, main_muscle_group=chest)
    cable_crossovers.equipment_needed.add(exercise_atlas)
    barbell_benchpress = Exercise.objects.create(name='Barbell benchpress', owner=request.user, main_muscle_group=chest)
    barbell_benchpress.equipment_needed.add(barbell, bench)
    dumbell_benchpress = Exercise.objects.create(name='Dumbell benchpress', owner=request.user, main_muscle_group=chest)
    dumbell_benchpress.equipment_needed.add(dumbells, bench)
    #upper back
    upper_back = Muscle.objects.get(name="Upper back")
    cable_crossovers_reverse = Exercise.objects.create(name='Cable crossovers reverse', owner=request.user, main_muscle_group=upper_back)
    cable_crossovers_reverse.equipment_needed.add(exercise_atlas)
    chin_ups = Exercise.objects.create(name='Chin-ups', owner=request.user, main_muscle_group=upper_back)
    chin_ups.equipment_needed.add(pull_up_bar)
    pull_ups = Exercise.objects.create(name='Pull-ups', owner=request.user, main_muscle_group=upper_back)
    pull_ups.equipment_needed.add(pull_up_bar)
    machine_pull_ups = Exercise.objects.create(name='Machine pull-ups', owner=request.user, main_muscle_group=upper_back)
    machine_pull_ups.equipment_needed.add(dip_pull_up_machine)
    machine_chin_ups = Exercise.objects.create(name='Machine chin-ups', owner=request.user, main_muscle_group=upper_back)
    machine_chin_ups.equipment_needed.add(dip_pull_up_machine)
    seated_cable_row = Exercise.objects.create(name='Seated cable row', owner=request.user, main_muscle_group=upper_back)
    seated_cable_row.equipment_needed.add(exercise_atlas)
    shrugs = Exercise.objects.create(name='Shrugs', owner=request.user, main_muscle_group=upper_back)
    shrugs.equipment_needed.add(barbell)
    lat_pull_down = Exercise.objects.create(name='Lat pull-down', owner=request.user, main_muscle_group=upper_back)
    lat_pull_down.equipment_needed.add(exercise_atlas)
    skier = Exercise.objects.create(name='Skier', owner=request.user, main_muscle_group=upper_back)
    skier.equipment_needed.add(exercise_atlas)
    dumbell_row = Exercise.objects.create(name='Dumbell row', owner=request.user, main_muscle_group=upper_back)
    dumbell_row.equipment_needed.add(dumbells)
    barbell_row = Exercise.objects.create(name='Barbell row', owner=request.user, main_muscle_group=upper_back)
    barbell_row.equipment_needed.add(barbell)
    #lower back
    lower_back = Muscle.objects.get(name='Lower back')
    deadlift = Exercise.objects.create(name='Deadlift', owner=request.user, main_muscle_group=lower_back)
    deadlift.equipment_needed.add(barbell)
    deadlift.equipment_needed.add(load)
    good_mornings = Exercise.objects.create(name="Good mornings", owner=request.user, main_muscle_group=lower_back)
    good_mornings.equipment_needed.add(barbell)

    #shoulders
    shoulder = Muscle.objects.get(name='Shoulder')
    face_pull = Exercise.objects.create(name='Face pull', owner=request.user, main_muscle_group=shoulder)
    face_pull.equipment_needed.add(exercise_atlas)
    machine_reverse_flies = Exercise.objects.create(name='Machine reverse flies', owner=request.user, main_muscle_group=shoulder)
    machine_reverse_flies.equipment_needed.add(fly_machine)
    seated_dumbell_press = Exercise.objects.create(name="Seated dumbell press", owner=request.user, main_muscle_group=shoulder)
    seated_dumbell_press.equipment_needed.add(dumbells, bench)
    barbell_raises = Exercise.objects.create(name="Barbell raises", owner=request.user, main_muscle_group=shoulder)
    barbell_raises.equipment_needed.add(barbell)
    dumbell_lateral_raises = Exercise.objects.create(name="Dumbell lateral raises", owner=request.user, main_muscle_group=shoulder)
    dumbell_lateral_raises.equipment_needed.add(dumbells)
    cable_row_lateral_raises = Exercise.objects.create(name="Cable row lateral raises", owner=request.user, main_muscle_group=shoulder)
    cable_row_lateral_raises.equipment_needed.add(exercise_atlas)
    overhead_press = Exercise.objects.create(name="Overhead press", owner=request.user, main_muscle_group=shoulder)
    overhead_press.equipment_needed.add(barbell)
    y_raises = Exercise.objects.create(name="Y-raises", owner=request.user, main_muscle_group=shoulder)
    y_raises.equipment_needed.add(dumbells, bench)
    dumbell_reverse_chest_flies = Exercise.objects.create(name="Dumbell reverse chest flies", owner=request.user, main_muscle_group=shoulder)
    dumbell_reverse_chest_flies.equipment_needed.add(dumbells, bench)
    #quads
    quads = Muscle.objects.get(name='Quads')
    leg_press = Exercise.objects.create(name="Leg press", owner=request.user, main_muscle_group=quads)
    leg_press.equipment_needed.add(leg_press_machine)
    highbar_squat = Exercise.objects.create(name="Highbar Squat", owner=request.user, main_muscle_group=quads)
    highbar_squat.equipment_needed.add(barbell, load)
    front_squat = Exercise.objects.create(name="Front Squat", owner=request.user, main_muscle_group=quads)
    front_squat.equipment_needed.add(barbell, load)
    goblet_squat = Exercise.objects.create(name="Goblet Squat", owner=request.user, main_muscle_group=quads)
    front_squat.equipment_needed.add(dumbells)
    #glutes and hamstrings
    glutes_hamstrings = Muscle.objects.get(name='Glutes and Hamstrings')
    lounges = Exercise.objects.create(name="Lounges", owner=request.user, main_muscle_group=glutes_hamstrings)
    lounges.equipment_needed.add(dumbells)
    hipthrust = Exercise.objects.create(name="Hipthrust", owner=request.user, main_muscle_group=glutes_hamstrings)
    hipthrust.equipment_needed.add(bench, barbell, load)
    lowbar_squat = Exercise.objects.create(name="Lowbar Squat", owner=request.user, main_muscle_group=glutes_hamstrings)
    lowbar_squat.equipment_needed.add(barbell, load)
    stiff_leg_deadlift = Exercise.objects.create(name="Stiff leg deadlift", owner=request.user, main_muscle_group=glutes_hamstrings)
    stiff_leg_deadlift.equipment_needed.add(barbell)
    #abdominal
    abdominal = Muscle.objects.get(name='Abdominal')
    leg_raises = Exercise.objects.create(name="Leg raises", owner=request.user, main_muscle_group=abdominal)
    leg_raises.equipment_needed.add(pull_up_bar)
    cable_crunch = Exercise.objects.create(name="Cable crunch", owner=request.user, main_muscle_group=abdominal)
    cable_crunch.equipment_needed.add(exercise_atlas)
    leg_crunches = Exercise.objects.create(name="Leg crunches", owner=request.user, main_muscle_group=abdominal)
    leg_crunches.equipment_needed.add(tricep_dip_bar)
    #tricep
    tricep = Muscle.objects.get(name='Tricep')
    tricep_dips = Exercise.objects.create(name="Tricep dips", owner=request.user, main_muscle_group=tricep)
    tricep_dips.equipment_needed.add(tricep_dip_bar)
    cable_tricep_extensions = Exercise.objects.create(name="Cable tricep extensions", owner=request.user, main_muscle_group=tricep)
    cable_tricep_extensions.equipment_needed.add(exercise_atlas)
    overhead_dumbell_tricep_extension = Exercise.objects.create(name="Overhead dumbell tricep extension", owner=request.user, main_muscle_group=tricep)
    overhead_dumbell_tricep_extension.equipment_needed.add(dumbells)
    overhead_barbell_tricep_extension = Exercise.objects.create(name="Overhead barbell tricep extension", owner=request.user, main_muscle_group=tricep)
    overhead_barbell_tricep_extension.equipment_needed.add(barbell)
    close_grip_barbell_benchpress = Exercise.objects.create(name="Close grip barbell benchpress", owner=request.user, main_muscle_group=tricep)
    close_grip_barbell_benchpress.equipment_needed.add(barbell, bench)
    close_grip_dumbell_benchpress = Exercise.objects.create(name="Close grip dumbell benchpress", owner=request.user, main_muscle_group=tricep)
    close_grip_dumbell_benchpress.equipment_needed.add(dumbells, bench)
    #bicep
    bicep = Muscle.objects.get(name='Bicep')
    dumbell_curls = Exercise.objects.create(name="Dumbell curls", owner=request.user, main_muscle_group=bicep)
    dumbell_curls.equipment_needed.add(dumbells)
    barbell_curls = dumbell_curls = Exercise.objects.create(name="Barbell curls", owner=request.user, main_muscle_group=bicep)
    barbell_curls.equipment_needed.add(barbell)
    hercules = dumbell_curls = Exercise.objects.create(name="Hercules", owner=request.user, main_muscle_group=bicep)
    hercules.equipment_needed.add(exercise_atlas)
    cable_curls = Exercise.objects.create(name="Cable curls", owner=request.user, main_muscle_group=bicep)
    cable_curls.equipment_needed.add(exercise_atlas)
    #calves
    calves = Muscle.objects.get(name="Calves")
    standing_barbell_calves_raise = Exercise.objects.create(name="Standing barbell calves raise", owner=request.user, main_muscle_group=calves)
    standing_barbell_calves_raise.equipment_needed.add(barbell)


def populate_templates_on_registration(request):
    deadlift = Exercise.objects.get(name='Deadlift', owner=request.user)
    barbell_row = Exercise.objects.get(name='Barbell row', owner=request.user)
    benchpress = Exercise.objects.get(name='Barbell benchpress', owner=request.user)
    seated_dumbell_press = Exercise.objects.get(name="Seated dumbell press", owner=request.user)
    dumbell_lateral_raises = Exercise.objects.get(name='Dumbell lateral raises', owner=request.user)
    barbell_curls = Exercise.objects.get(name='Barbell curls', owner=request.user)
    close_grip_dumbell_benchpress = Exercise.objects.get(name="Close grip dumbell benchpress", owner=request.user)
    # Home Gym Full Body Workout A
    home_gym_fbw_A = WorkoutTemplate.objects.create(name='Home Gym Full Body Workout A', owner=request.user, sample=True)
    home_gym_fbw_A_workout = Workout.objects.create(owner=request.user, template=home_gym_fbw_A, is_template=True, finished=True)
    home_gym_fbw_A_workout_deadlift = WorkoutExercise.objects.create(owner=request.user, exercise=deadlift, workout=home_gym_fbw_A_workout, order=1)
    deadlift_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_deadlift, repetitions=5, order=1)
    deadlift_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_deadlift, repetitions=5, order=2)
    deadlift_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_deadlift, repetitions=5, order=3)
    home_gym_fbw_A_workout_barbell_row = WorkoutExercise.objects.create(owner=request.user, exercise=barbell_row, workout=home_gym_fbw_A_workout, order=2)
    barbell_row_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_row, repetitions=5, order=1)
    barbell_row_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_row, repetitions=5, order=2)
    barbell_row_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_row, repetitions=5, order=3)
    home_gym_fbw_A_workout_barbell_benchpress = WorkoutExercise.objects.create(owner=request.user, exercise=benchpress, workout=home_gym_fbw_A_workout, order=3)
    barbell_benchpress_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_benchpress, repetitions=8, order=1)
    barbell_benchpress_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_benchpress, repetitions=8, order=2)
    barbell_benchpress_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_benchpress, repetitions=8, order=3)
    home_gym_fbw_A_workout_seated_dumbell_press = WorkoutExercise.objects.create(owner=request.user, exercise=seated_dumbell_press, workout=home_gym_fbw_A_workout, order=4)
    seated_dumbell_press_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_seated_dumbell_press, repetitions=8, order=1)
    seated_dumbell_press_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_seated_dumbell_press, repetitions=8, order=2)
    seated_dumbell_press_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_seated_dumbell_press, repetitions=8, order=3)
    home_gym_fbw_A_workout_dumbell_lateral_raises = WorkoutExercise.objects.create(owner=request.user, exercise=dumbell_lateral_raises, workout=home_gym_fbw_A_workout, order=5)
    dumbell_lateral_raises_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_dumbell_lateral_raises, repetitions=12, order=1)
    dumbell_lateral_raises_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_dumbell_lateral_raises, repetitions=12, order=2)
    dumbell_lateral_raises_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_dumbell_lateral_raises, repetitions=12, order=3)
    home_gym_fbw_A_workout_barbell_curls = WorkoutExercise.objects.create(owner=request.user, exercise=barbell_curls, workout=home_gym_fbw_A_workout, order=6)
    barbell_curls_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_curls, repetitions=12, order=1)
    barbell_curls_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_curls, repetitions=12, order=2)
    barbell_curls_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_barbell_curls, repetitions=12, order=3)
    home_gym_fbw_A_workout_close_grip_dumbell_benchpress = WorkoutExercise.objects.create(owner=request.user, exercise=close_grip_dumbell_benchpress, workout=home_gym_fbw_A_workout, order=7)
    close_grip_dumbell_benchpress_set_1 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_close_grip_dumbell_benchpress, repetitions=12, order=1)
    close_grip_dumbell_benchpress_set_2 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_close_grip_dumbell_benchpress, repetitions=12, order=2)
    close_grip_dumbell_benchpress_set_3 = Set.objects.create(owner=request.user, workout_exercise=home_gym_fbw_A_workout_close_grip_dumbell_benchpress, repetitions=12, order=3)