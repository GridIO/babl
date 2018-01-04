import { Component, Injectable, Inject } from '@angular/core';
import { NavController } from 'ionic-angular';

import { UsersService } from "../../app/services/users.service";
import { Person } from '../../app/models/person';

import { ProfilePage } from "../profile/profile";

@Component({
  selector: 'page-people',
  templateUrl: 'people.html'
})
export class PeoplePage {

  grid: Array<Array<Person>>;
  rowNum: Array<number> = [];

  constructor(public navCtrl: NavController, private peopleService: UsersService) { }

  getPeople(): void {
    this.peopleService.getNearby()
        .subscribe(
          response => {

            // reset data
            try {
              if (this.grid.length > 0 || this.rowNum.length > 0) {
                this.grid.length = 0;
                this.rowNum.length = 0;
              }
            }
            catch(err) {
              console.log('No data yet, getting it for the first time...');
            }

            // create grid
            let grid = [];

            for (let i = 0; i < response.count; i += 3) {
              grid.push(response.results.slice(i, i+3));
            }

            this.grid = grid;


            // get row count to create grid
            for (let i = 0; i < grid.length; i++) {
              this.rowNum.push(i);
            }

          },
          err => {
            console.log(err);
          })
  }

  ionViewDidLoad() {
    this.getPeople();
  }

  doRefresh(refresher) {
    console.log('Begin async operation', refresher);

    setTimeout(() => {
      console.log('Async operation has ended');

      // get new data
      this.getPeople();
      refresher.complete();
    }, 2000);
  }

  goToProfile(person: Person) {
    this.navCtrl.push(ProfilePage, person);
  }

}
