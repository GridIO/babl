import { Component, ViewChild }                               from '@angular/core';
import { NavController, NavParams, Content, AlertController } from 'ionic-angular';


import { MessageService }                                     from "../../app/services/messages.service";
import { Message }                                            from "../../app/models/message";

import { Person }                                             from "../../app/models/person";


@Component({
  selector: 'page-messaging',
  templateUrl: 'messaging.html',
})
export class MessagingPage {
  @ViewChild(Content) content: Content;

  profile: Person;
  messages: Message[];
  newMessage = {
    message_type: null,
    sender_content: null,
    image: null
  };
  tabBarElement: any;
  nextUrl: string;

  constructor(
    public navCtrl: NavController, public navParams: NavParams, private messageService: MessageService,
    public alertCtrl: AlertController
  ) {
    this.profile = navParams.data;
    this.getMessages();
    this.tabBarElement = document.querySelector('.tabbar.show-tabbar');
    this.messages = new Array<Message>();
  }

  // hides tabBar when the page is displayed
  ionViewWillEnter() {
    this.tabBarElement.style.display = 'none';
  }

  // scrolls to bottom whenever the page has loaded
  ionViewDidEnter() {
    this.content.scrollToBottom(0);
  }

  // shows tabBar again when moving away from the page
  ionViewWillLeave() {
    this.tabBarElement.style.display = 'flex';
  }

  getMessages(): void {
    // initialize a currentUrl
    let currentUrl: string;

    // ensure that a url override is specified if there's already more to get
    if (this.nextUrl) {
      currentUrl = this.nextUrl;
    } else {
      currentUrl = null;
    }

    this.messageService.getMessages(this.profile.id, currentUrl)
        .subscribe(
          response => {
            let results = response.results.sort(function (a, b) {
              let keyA = new Date(a.sent_at),
                  keyB = new Date(b.sent_at);
              // Compare the 2 dates
              if(keyA < keyB) return -1;
              if(keyA > keyB) return 1;
              return 0;
            });

            // add results from API pull to the messages list if not all have been received
            if (this.messages.length < response.count) {
              this.messages = results.concat(this.messages);
            }

            // make sure that the nextUrl to grab is the one from response.next
            console.log(this.messages);
            this.nextUrl = response.next;

          },
          err => {
            console.log(err);
          })
  }

  attachImage() {
    // todo: need to actually implement this
    let alert = this.alertCtrl.create({
      title: 'Under construction',
      subTitle: 'This feature is currently under construction, check back later!',
      buttons: ['Got it!']
    });
    alert.present();
  }

  sendMessage() {
    // set media type
    if (this.newMessage.sender_content) {
      this.newMessage.message_type = 'txt'
    }
    else if (this.newMessage.image) {
      this.newMessage.message_type = 'img'
    }

    // Send message
    this.messageService.sendMessage(this.profile.id, this.newMessage)
        .subscribe(
          response => {
            console.log(response);

            this.messages.push(response);
            this.content.scrollToBottom(0);
          },
          err => {
            console.log(err);
          })

    // Empty out newMessage object
    this.newMessage.message_type = null;
    this.newMessage.sender_content = null;
    this.newMessage.image = null;
  }

  doInfinite(infiniteScroll) {
    console.log('Begin async operation');

    setTimeout(() => {
      this.getMessages();

      console.log('Async operation has ended');
      infiniteScroll.complete();

    }, 500);


  }

}
