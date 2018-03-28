import { Component }                from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

import { UsersService }             from "../../app/services/users.service";
import { Person, Attributes }       from "../../app/models/person";

import { MessagingPage }            from "../messaging/messaging";
import { EditProfilePage }          from "../edit-profile/edit-profile";
import { SettingsPage }             from "../settings/settings";

@Component({
  selector: 'page-profile',
  templateUrl: 'profile.html'
})
export class ProfilePage {

  profile: Person;
  isCurrentUser: boolean;
  attributes: object;

  constructor(public navCtrl: NavController, public navParams: NavParams, private usersService: UsersService) {

    // if there's navParams specified, then use that as the profile
    // else use logged in user
    if (navParams.data && (Object.keys(navParams.data).length === 0)) {
      this.getCurrentUser();
      this.isCurrentUser = true;
    }
    else {
      this.profile = navParams.data;
      this.isCurrentUser = false;
    }

    // grab user attributes for use when building view
    this.attributes = Attributes;

  }

  getCurrentUser(): void {
    this.usersService.getMe()
        .subscribe(
          response => {
            this.profile = response.results[0];
          },
          err => {
            console.log(err);
          })
  }

  goToSettings(person: Person) {
    if (person) {
      this.navCtrl.push(SettingsPage, person);
    }
    else {
      // do nothing
    }
  }

  goToMessages(person: Person) {
    if (person) {
      this.navCtrl.push(MessagingPage, person);
    }
    else {
      // do nothing
    }
  }

  editProfile(person: Person) {
    if (person) {
      this.navCtrl.push(EditProfilePage, person);
    }
    else {
      // do nothing
    }

  }

}
