#!/usr/bin/env python3
# added this comment
"""
Simple Todo List Application
A command-line todo list manager that allows users to:
- Add new tasks
- List all tasks
- Mark tasks as done
- Save and load tasks from a file
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class TodoList:
    """A simple todo list manager."""
    
    def __init__(self, filename: str = "todos.json"):
        """Initialize the todo list with a data file."""
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading {self.filename}. Starting with empty list.")
                return []
        return []
    
    def save_tasks(self) -> None:
        """Save tasks to the JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, indent=2, ensure_ascii=False)
        except IOError:
            print(f"Error saving to {self.filename}")
    
    def add_task(self, description: str) -> None:
        """Add a new task to the list."""
        if not description.strip():
            print("Task description cannot be empty!")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Added task: {description.strip()}")
    
    def list_tasks(self) -> None:
        """Display all tasks in the list."""
        if not self.tasks:
            print("No tasks found. Add some tasks to get started!")
            return
        
        print("\n" + "="*50)
        print("📋 YOUR TODO LIST")
        print("="*50)
        
        for task in self.tasks:
            status = "✅" if task["completed"] else "⏳"
            print(f"{task['id']:2d}. {status} {task['description']}")
        
        completed_count = sum(1 for task in self.tasks if task["completed"])
        total_count = len(self.tasks)
        print(f"\nProgress: {completed_count}/{total_count} tasks completed")
        print("="*50)
    
    def mark_done(self, task_id: int) -> None:
        """Mark a task as completed."""
        if not self.tasks:
            print("No tasks to mark as done!")
            return
        
        # Find task by ID
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        
        if task is None:
            print(f"Task with ID {task_id} not found!")
            return
        
        if task["completed"]:
            print(f"Task '{task['description']}' is already completed!")
            return
        
        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat()
        self.save_tasks()
        print(f"✓ Marked as done: {task['description']}")
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending (incomplete) tasks."""
        return [task for task in self.tasks if not task["completed"]]
    
    def get_completed_tasks(self) -> List[Dict[str, Any]]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task["completed"]]


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*40)
    print("🎯 TODO LIST MANAGER")
    print("="*40)
    print("1. Add a new task")
    print("2. List all tasks")
    print("3. Mark task as done")
    print("4. Show pending tasks only")
    print("5. Show completed tasks only")
    print("6. Exit")
    print("="*40)


def get_user_choice() -> str:
    """Get user's menu choice."""
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return '6'


def main():
    """Main application loop."""
    print("Welcome to the Todo List Manager! 🚀")
    
    todo_list = TodoList()
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':  # Add task
            description = input("Enter task description: ").strip()
            todo_list.add_task(description)
        
        elif choice == '2':  # List all tasks
            todo_list.list_tasks()
        
        elif choice == '3':  # Mark task as done
            if not todo_list.tasks:
                print("No tasks available to mark as done!")
                continue
            
            # Show pending tasks for reference
            pending = todo_list.get_pending_tasks()
            if not pending:
                print("All tasks are already completed! 🎉")
                continue
            
            print("\nPending tasks:")
            for task in pending:
                print(f"  {task['id']}. {task['description']}")
            
            try:
                task_id = int(input("\nEnter task ID to mark as done: "))
                todo_list.mark_done(task_id)
            except ValueError:
                print("Please enter a valid task ID number.")
        
        elif choice == '4':  # Show pending tasks only
            pending = todo_list.get_pending_tasks()
            if not pending:
                print("No pending tasks! 🎉")
            else:
                print("\n📋 PENDING TASKS:")
                print("-" * 30)
                for task in pending:
                    print(f"{task['id']:2d}. ⏳ {task['description']}")
        
        elif choice == '5':  # Show completed tasks only
            completed = todo_list.get_completed_tasks()
            if not completed:
                print("No completed tasks yet.")
            else:
                print("\n✅ COMPLETED TASKS:")
                print("-" * 30)
                for task in completed:
                    print(f"{task['id']:2d}. ✅ {task['description']}")
        
        elif choice == '6':  # Exit
            print("\nThanks for using Todo List Manager! 👋")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again or contact support.")