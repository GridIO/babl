import { NgModule, ErrorHandler }                   from '@angular/core';
import { BrowserModule }                            from '@angular/platform-browser';
import { IonicApp, IonicModule, IonicErrorHandler } from 'ionic-angular';
import { MyApp }                                    from './app.component';
import { IonicStorageModule }                       from '@ionic/storage';

import { PeoplePage }                               from '../pages/people/people';
import { ChatsPage }                                from '../pages/chats/chats';
import { ProfilePage }                              from '../pages/profile/profile';
import { TabsPage }                                 from '../pages/tabs/tabs';
import { MessagingPage }                            from '../pages/messaging/messaging';
import { EditProfilePage }                          from '../pages/edit-profile/edit-profile';
import { SettingsPage }                             from "../pages/settings/settings";

import { LoginPage }                                from "../pages/login/login";

import { StatusBar }                                from '@ionic-native/status-bar';
import { SplashScreen }                             from '@ionic-native/splash-screen';

import { HttpClientModule }                         from '@angular/common/http';
import { UsersService }                             from "./services/users.service";
import { MessageService }                           from "./services/messages.service";
import { AuthenticationService }                    from "./services/authentication.service";

@NgModule({
  declarations: [
    MyApp,
    PeoplePage,
    ChatsPage,
    ProfilePage,
    TabsPage,
    MessagingPage,
    EditProfilePage,
    SettingsPage,
    LoginPage,
  ],
  imports: [
    BrowserModule,
    IonicModule.forRoot(MyApp),
    IonicStorageModule.forRoot(),
    HttpClientModule,
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    PeoplePage,
    ChatsPage,
    ProfilePage,
    TabsPage,
    MessagingPage,
    EditProfilePage,
    SettingsPage,
    LoginPage,
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    UsersService,
    MessageService,
    AuthenticationService
  ]
})
export class AppModule {}
