import { Component }    from '@angular/core';
import { Platform }     from 'ionic-angular';
import { StatusBar }    from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { Storage }      from "@ionic/storage";

import { TabsPage }     from '../pages/tabs/tabs';
import { LoginPage }    from "../pages/login/login";

@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  public rootPage: any;

  constructor(platform: Platform, statusBar: StatusBar, splashScreen: SplashScreen, storage: Storage) {
    platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      statusBar.styleDefault();
      splashScreen.hide();

      storage.get('auth:token').then((authToken) => {

        if (authToken) {
          this.rootPage = TabsPage;
        } else {
          this.rootPage = LoginPage;
        }

      });


    });
  }
}
