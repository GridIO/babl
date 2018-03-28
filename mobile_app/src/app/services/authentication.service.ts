import { Injectable }     from '@angular/core';
import { Observable }     from 'rxjs/Rx';

import { APP_CONFIG }     from "../../app/app-config";

import { GenericService } from "./service-helper";



@Injectable()
export class AuthenticationService extends GenericService {

  private login_endpoint: string = APP_CONFIG.apiEndpoint + '/login/';


  login(body): Observable<any> {
    return this.post(this.login_endpoint, body);
  }

  // register(): Observable<any> {
  //   // todo
  // }

}
