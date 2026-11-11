
from dataclasses import dataclass
from datetime import date
from drafter import *


# Dataclass for each assignment
@dataclass
class Assignment:
    title: str
    subject: str
    due_date: str
    completed: bool


# Dataclass for each study goal
@dataclass
class StudyGoal:
    description: str
    subject: str
    completed: bool


# Main program state
@dataclass
class State:
    assignments: list[Assignment]
    study_goals: list[StudyGoal]
    selected_subject: str
    message: str
    student_name: str
    show_completed: bool


# HOME PAGE
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("My Study Planner"),
        "Welcome to your personal study planner!",
        "\nStay organized, track assignments, and reach your goals.",
        "\n\n" + state.message,
        Header("Navigation", level=2),
        Button("View Assignments", "assignments"),
        Button("Add Assignment", "add_assignment"),
        Button("Study Goals", "goals"),
        Button("Add Study Goal", "add_goal"),
        Button("View Progress", "progress"),
        "\n\nUse this website to stay on top of your schoolwork!"
    ])


# VIEW ASSIGNMENTS PAGE
@route
def assignments(state: State) -> Page:
    content = [
        Header("My Assignments"),
        state.message,
        "\nFilter assignments by subject:",
        SelectBox(
            "subject",
            ["All", "Math", "Science", "English", "History",
             "Programming", "Other"],
            state.selected_subject
        ),
        Button("Apply Filter", "filter_assignments"),
        "\n"
    ]

    today = date.today().isoformat()
    found = False

    # Display assignments that match the selected subject
    for index, assignment in enumerate(state.assignments):
        if (state.selected_subject == "All" or
                assignment.subject == state.selected_subject):

            found = True
            content.append(Header(assignment.title, level=3))
            content.append("Subject: " + assignment.subject)
            content.append("\nDue date: " + assignment.due_date)

            if assignment.completed:
                content.append("\nStatus: Completed")
            elif assignment.due_date < today:
                content.append("\nStatus: Overdue")
            else:
                content.append("\nStatus: In progress")

            content.append("\n")
            content.append(Button(
                "Change Completion Status",
                "toggle_assignment",
                arguments={"assignment_index": index}
            ))
            content.append("\n\n")

    if not found:
        content.append("No assignments found.")

    content.extend([
        "\n",
        Button("Add Assignment", "add_assignment"),
        Button("Home", "index")
    ])

    return Page(state, content)


# ADD ASSIGNMENT PAGE
@route
def add_assignment(state: State) -> Page:
    return Page(state, [
        Header("Add a New Assignment"),
        "Enter the assignment information below.",
        "\nAssignment title:",
        TextBox("title"),
        "\nSubject:",
        SelectBox(
            "subject",
            ["Math", "Science", "English", "History",
             "Programming", "Other"]
        ),
        "\nDue date:",
        TextBox("due_date", "", kind="date"),
        "\nIs this assignment already completed?",
        CheckBox("completed"),
        "\n",
        Button("Save Assignment", "save_assignment"),
        Button("Back to Assignments", "assignments"),
        Button("Home", "index")
    ])


# SAVE ASSIGNMENT ROUTE
@route
def save_assignment(state: State, title: str,
                    subject: str, due_date: str,
                    completed: bool) -> Page:

    if title.strip() == "":
        state.message = "Please enter an assignment title."
        return add_assignment(state)

    elif due_date == "":
        state.message = "Please select a due date."
        return add_assignment(state)

    else:
        new_assignment = Assignment(
            title.strip(),
            subject,
            due_date,
            completed
        )

        state.assignments.append(new_assignment)
        state.message = "Your assignment was added successfully!"

        return assignments(state)


# CHANGE ASSIGNMENT COMPLETION
@route
def toggle_assignment(state: State,
                      assignment_index: int) -> Page:

    assignment = state.assignments[assignment_index]
    assignment.completed = not assignment.completed

    state.message = "Assignment status updated!"

    return assignments(state)


# FILTER ASSIGNMENTS
@route
def filter_assignments(state: State, subject: str) -> Page:
    state.selected_subject = subject
    state.message = "Assignments filtered by " + subject + "."

    return assignments(state)


# STUDY GOALS PAGE
@route
def goals(state: State) -> Page:
    content = [
        Header("My Study Goals"),
        state.message,
        "\nHere are your current study goals:\n"
    ]

    if len(state.study_goals) == 0:
        content.append("You have not added any study goals yet.")

    # Display every study goal
    for index, goal in enumerate(state.study_goals):
        content.append(Header(goal.description, level=3))
        content.append("Subject: " + goal.subject)

        if goal.completed:
            content.append("\nStatus: Completed")
        else:
            content.append("\nStatus: In progress")

        content.append("\n")
        content.append(Button(
            "Change Goal Status",
            "toggle_goal",
            arguments={"goal_index": index}
        ))
        content.append("\n\n")

    content.extend([
        Button("Add Study Goal", "add_goal"),
        Button("View Progress", "progress"),
        Button("Home", "index")
    ])

    return Page(state, content)


# ADD STUDY GOAL PAGE
@route
def add_goal(state: State) -> Page:
    return Page(state, [
        Header("Create a Study Goal"),
        "What would you like to accomplish?",
        "\nStudy goal:",
        TextArea("description", "", rows=4),
        "\nChoose a subject:",
        SelectBox(
            "subject",
            ["Math", "Science", "English", "History",
             "Programming", "Other"]
        ),
        "\n",
        Button("Save Goal", "save_goal"),
        Button("View Goals", "goals"),
        Button("Home", "index")
    ])


# SAVE STUDY GOAL ROUTE
@route
def save_goal(state: State, description: str,
              subject: str) -> Page:

    if description.strip() == "":
        state.message = "Please enter a study goal."
        return add_goal(state)

    else:
        new_goal = StudyGoal(
            description.strip(),
            subject,
            False
        )

        state.study_goals.append(new_goal)
        state.message = "Your study goal was saved!"

        return goals(state)


# CHANGE STUDY GOAL COMPLETION
@route
def toggle_goal(state: State, goal_index: int) -> Page:

    goal = state.study_goals[goal_index]
    goal.completed = not goal.completed

    state.message = "Study goal status updated!"

    return goals(state)


# PROGRESS PAGE
@route
def progress(state: State) -> Page:
    completed_assignments = 0
    completed_goals = 0

    # Count completed assignments
    for assignment in state.assignments:
        if assignment.completed:
            completed_assignments += 1

    # Count completed study goals
    for goal in state.study_goals:
        if goal.completed:
            completed_goals += 1

    total_assignments = len(state.assignments)
    total_goals = len(state.study_goals)

    content = [
        Header("My Progress"),
        "Track how much you have accomplished!",
        Header("Assignment Progress", level=2),
        "Completed assignments: " +
        str(completed_assignments),
        "\nTotal assignments: " + str(total_assignments),
        "\n"
    ]

    if total_assignments > 0:
        percentage = (completed_assignments /
                      total_assignments) * 100
        content.append(
            "Assignment completion: " +
            str(round(percentage, 1)) + "%"
        )
    else:
        content.append("You have not added any assignments yet.")

    content.extend([
        "\n",
        Header("Study Goal Progress", level=2),
        "Completed goals: " + str(completed_goals),
        "\nTotal study goals: " + str(total_goals),
        "\n"
    ])

    if total_goals > 0:
        goal_percentage = (completed_goals / total_goals) * 100
        content.append(
            "Goal completion: " +
            str(round(goal_percentage, 1)) + "%"
        )
    else:
        content.append("You have not added any study goals yet.")

    content.extend([
        "\n",
        Button("View Assignments", "assignments"),
        Button("View Study Goals", "goals"),
        Button("Home", "index")
    ])

    return Page(state, content)


# START THE WEBSITE
start_server(
    State(
        [],
        [],
        "All",
        "Welcome! Start by adding an assignment.",
        "",
        False
    ),
    site_title="My Study Planner"
)
