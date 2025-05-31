class User:
    def __init__(self, username="anonymous"):
        self.username = username
        self.__user_history = []
    
    def append_to_user_history(self, question: str):
        """Records a question asked by the user."""
        self.__user_history.append(question)
    
    def get_history(self):
        """Returns the user's interaction history."""
        return self.__user_history
    
    def clear_history(self):
        """Clears the user's interaction history."""
        self.__user_history.clear()
    
    def print_history(self):
        """Prints the user's interaction history."""
        print(f"Interaction history for {self.susername}:")
        for line in self.__user_history:
            print(line)