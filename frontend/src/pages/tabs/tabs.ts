import { Component } from '@angular/core';

import { AboutPage } from '../about/about';
import { ContactPage } from '../contact/contact';
import { MyProfile } from '../myprofile/myprofile';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = MyProfile;
  tab2Root = AboutPage;
  tab3Root = ContactPage;

  constructor() {

  }
}
