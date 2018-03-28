import { Component }                from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

import { Person }                   from "../../app/models/person";

import { UsersService }             from "../../app/services/users.service";


@Component({
  selector: 'page-edit-profile',
  templateUrl: 'edit-profile.html',
})
export class EditProfilePage {

  profile: Person;

  constructor(public navCtrl: NavController, public navParams: NavParams, private usersService: UsersService) {
    this.profile = navParams.data;
    console.log(navParams.data);
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EditProfilePage');
  }

  save() {
    console.log(this.profile);
    this.usersService.patchProfile(this.profile.id, this.profile)
        .subscribe(
          response => {
            console.log(response);

            this.navCtrl.pop();
          },
          err => {
           console.log(err);
          })
  }

}
