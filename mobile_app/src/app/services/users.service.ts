import { Injectable }     from '@angular/core';
import { Observable }     from 'rxjs/Rx';

import { APP_CONFIG }     from "../../app/app-config";

import { PersonResponse } from '../models/person';

import { GenericService } from "./service-helper";



@Injectable()
export class UsersService extends GenericService {

  private base_endpoint: string = APP_CONFIG.apiEndpoint + '/users/';
  private me_endpoint: string = APP_CONFIG.apiEndpoint + '/users/me/';
  private nearby_endpoint: string = APP_CONFIG.apiEndpoint + '/users/closest/';
  private conversations_endpoint: string = APP_CONFIG.apiEndpoint + '/users/conversations/';


  getNearby(): Observable<PersonResponse> {
    return this.get(this.nearby_endpoint);
  }

  getMe(): Observable<PersonResponse> {
    return this.get(this.me_endpoint);
  }

  getConversations(): Observable<PersonResponse> {
    return this.get(this.conversations_endpoint);
  }

  patchProfile(user_id, body): Observable<any> {
    return this.patch(this.base_endpoint + user_id + '/', body)
  }

}
