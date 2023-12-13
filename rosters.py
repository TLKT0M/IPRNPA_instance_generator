def generate_roster(nurse_list, shifts, skill_nurses, max_shifts):
    from gurobipy import quicksum, Model, GRB
    from itertools import product

    nurses = [nurse["id"] for nurse in nurse_list]

    shift_night = [shift for shift in shifts if shift % 3 == 0]
    shift_late = [shift for shift in shifts if shift % 3 == 2]
    shift_morning = [shift for shift in shifts if shift % 3 == 1]

    modelOpt = Model("Nurse Rostering")

    # DECISION VARIABLES

    # assign_n,s,d: binary
    x = modelOpt.addVars(
        list(product(nurses, shifts)),
        vtype=GRB.BINARY,
        name="assignmentOfNursesToShifts",
    )

    # MATHEMATICAL MODEL

    # OBJECTIVE FUNCTION
    # (31) Minimisation of the assigned nurses to fulfill the requirements

    quicksum(x[(nurse, shift)] for nurse in nurses for shift in shifts)
    modelOpt.setObjective(x.sum("*", "*"), GRB.MINIMIZE)

    # Equations

    # (32) Each nurse can only work during at most one shift on each day

    modelOpt.addConstrs(
        (
            x[(nurse, shift)]
            + x[(nurse, shift + 1)]
            + x[(nurse, shift + 2)] <= 1
            for nurse in nurses
            for shift in shift_morning
        ),
        "max one shift per day",
    )

    # (33) The minimum number of nurses per type must be assigned per shift

    modelOpt.addConstrs(
        (
            quicksum(
                x[(nurse["id"], shift)]
                for nurse in nurse_list
                if nurse["skillLevel"] >= i
            )
            >= skill_nurses[shift - 1][i]
            for shift in shifts
            for i in range(len(skill_nurses[shift - 1]))
        ),
        "enough nurses per skill level",
    )

    # (34) The minimum total number of nurses must be assigned per shift

    modelOpt.addConstrs(
        (
            quicksum(x[(nurse["id"], shift)] for nurse in nurse_list)
            >= quicksum(
                skill_nurses[shift - 1][i]
                for i in range(len(skill_nurses[shift - 1]))
            )
            for shift in shifts
        ),
        "enough nurses per shift",
    )

    # (35) A nurse cannot exceed the maximum number of shifts
    # in the time horizon

    modelOpt.addConstrs(
        (
            quicksum(x[(nurse, shift)] for shift in shifts) <= max_shifts
            for nurse in nurses
        ),
        "Equations_35",
    )

    # (36) After a night shift a nurse can only have
    # another night shift (or the day off)

    modelOpt.addConstrs(
        (
            x[(nurse, shift)]
            + x[(nurse, shift + 1)]
            + x[(nurse, shift + 2)] <= 1
            for nurse in nurses
            for shift in shift_night[: len(shift_night) - 1]
        ),
        "shift pattern night shift",
    )

    # (37) After an evening shift a nurse cannot have a morning shift
    # on the next day

    modelOpt.addConstrs(
        (
            x[(nurse, shift)] + x[(nurse, shift + 2)] <= 1
            for nurse in nurses
            for shift in shift_late[: len(shift_late) - 1]
        ),
        "shift pattern morning shift",
    )

    # Execution Optimisation
    modelOpt.write("nurseRostering.lp")

    modelOpt.optimize()
    try:
        obj = modelOpt.getObjective()
        print("Objective = ", obj.getValue())
        for nurse in nurse_list:
            nurse["workingShifts"] = [
                shift
                for shift in shifts
                if int(x[(nurse["id"], shift)].X) > 0.99
            ]

        return nurse_list
    except AttributeError:
        raise ValueError("increase fix_nurses")
