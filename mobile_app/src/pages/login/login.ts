import { Component }                from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { Observable }               from "rxjs/Rx";
import { Storage }                  from "@ionic/storage";

import { AuthenticationService }    from "../../app/services/authentication.service";

import { TabsPage }                 from "../tabs/tabs";



@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  credentials: object = {};

  constructor(public navCtrl: NavController, public navParams: NavParams,
              private authService: AuthenticationService, private storage: Storage) {

  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad LoginPage');
  }

  login() {
    console.log(this.credentials);

    this.authService.login(this.credentials)
      .subscribe(
        response => {
          console.log(response);

          // if auth token received, go to TabsPage
          if (response.token) {
            this.storage.set('auth:token', response.token);
            this.navCtrl.setRoot(TabsPage);
          }

        },
        err => {
          console.log(err);
        });
  }

  register() {

  }


}
