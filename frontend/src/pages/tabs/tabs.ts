import { Component } from '@angular/core';

import { PeoplePage } from '../people/people';
import { ChatsPage } from '../chats/chats';
import { MyProfilePage } from '../myprofile/myprofile';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = MyProfilePage;
  tab2Root = PeoplePage;
  tab3Root = ChatsPage;

  constructor() {

  }
}
