import { Component }     from '@angular/core';
import { NavController } from 'ionic-angular';

import { UsersService }  from "../../app/services/users.service";
import { Person }        from "../../app/models/person";

import { MessagingPage } from "../messaging/messaging";


@Component({
  selector: 'page-chats',
  templateUrl: 'chats.html'
})
export class ChatsPage {

  conversations: Array<Person>;

  constructor(public navCtrl: NavController, private usersService: UsersService) { }

  getPeople(): void {
    this.usersService.getConversations()
        .subscribe(
          response => {

            // reset data
            try {
              if (this.conversations.length > 0) {
                this.conversations.length = 0;
              }
            }
            catch(err) {
              console.log('No data yet, getting it for the first time...')
            }

            // create list
            this.conversations = response.results;

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

  goToMessages(person: Person) {
    this.navCtrl.push(MessagingPage, person);
  }

}
