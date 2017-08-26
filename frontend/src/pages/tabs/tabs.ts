import { Component } from '@angular/core';

import { PeoplePage } from '../people/people';
import { ChatsPage } from '../chats/chats';
import { ProfilePage } from '../profile/profile';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = ProfilePage;
  tab2Root = PeoplePage;
  tab3Root = ChatsPage;

  constructor() {

  }
}
