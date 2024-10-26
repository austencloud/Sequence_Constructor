from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject
from .edit_user_profiles_dialog import EditUserProfilesDialog

if TYPE_CHECKING:
    from ..user_profile_settings import UserProfileSettings


class UserManager(QObject):
    def __init__(self, user_profile_settings: "UserProfileSettings"):
        super().__init__()
        self.user_profile_settings = user_profile_settings
        self.previous_user = ""
        self.user_combo_box = None

    def populate_user_profiles_combo_box(self, user_combo_box: QComboBox):
        user_profiles = self.user_profile_settings.get_user_profiles()
        current_user = self.user_profile_settings.get_current_user()
        self.user_combo_box = user_combo_box
        self.user_combo_box.clear()
        for user_name in user_profiles.keys():
            self.user_combo_box.addItem(user_name)
        self.user_combo_box.addItem("Edit Users")
        if current_user in user_profiles:
            index = self.user_combo_box.findText(current_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        self.user_combo_box.currentIndexChanged.connect(
            self._update_current_user_in_combo_box
        )

    def _update_current_user_in_combo_box(self):
        selected_user = self.user_combo_box.currentText()
        if selected_user == "Edit Users":
            self.open_edit_users_dialog()
        else:
            self.user_profile_settings.set_current_user(selected_user)

    def open_edit_users_dialog(self):
        dialog = EditUserProfilesDialog(self)
        if dialog.exec():
            self.populate_user_profiles_combo_box(self.user_combo_box)

    def get_all_users(self):
        return list(self.user_profile_settings.get_user_profiles().keys())

    def add_new_user(self, user_name):
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles:
            return False
        user_profiles[user_name] = {"name": user_name}
        self.user_profile_settings.set_user_profiles(user_profiles)
        self.user_profile_settings.set_current_user(user_name)
        return True

    def remove_user(self, user_name):
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles:
            del user_profiles[user_name]
            self.user_profile_settings.set_user_profiles(user_profiles)
            return True
        return False

    def save_users(self):
        # User data is directly saved with set_user_profiles method, no additional save needed
        pass

    def get_current_user(self):
        return self.user_profile_settings.get_current_user()

    def set_current_user(self, user_name):
        self.user_profile_settings.set_current_user(user_name)
