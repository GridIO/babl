import { Injectable }               from '@angular/core';
import { Observable }               from 'rxjs/Rx';

import { APP_CONFIG }               from "../../app/app-config";

import { MessageResponse }          from "../models/message";

import { GenericService }           from "./service-helper";



@Injectable()
export class MessageService extends GenericService {

  private message_endpoint: string = APP_CONFIG.apiEndpoint + '/messages/?recipient=';

  getMessages(recipient_id, url_override=null): Observable<MessageResponse> {

    if (url_override) {
      console.log('override worked');
      return this.get(url_override);
    }

    console.log('no override');
    return this.get(this.message_endpoint + recipient_id);
  }

  sendMessage(recipient_id, body): any {
    return this.post(this.message_endpoint + recipient_id, body);
  }
}
