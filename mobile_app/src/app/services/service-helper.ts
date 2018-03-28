import { Injectable }              from '@angular/core';
import { Observable }              from 'rxjs/Rx';

import { HttpClient, HttpHeaders } from '@angular/common/http';



@Injectable()
export class GenericService {

  constructor(private http: HttpClient) { }

  createAuthorizationHeader() {
    // todo: get auth token

    // append auth token to headers
    const headers = new HttpHeaders()
      .set("Authorization", 'Token 7f845c4db750d32d672fb2c21e64c9c9f729163c');

    return headers
  }

  get(url): Observable<any> {
    const options = {
      headers: this.createAuthorizationHeader()
    };

    return this.http.get(url, options)
      .map((response: Response) => response)
      .catch((error: any) => Observable.throw(error.error || 'Server error'));

  }

  post(url, body): Observable<any> {
    const options = {
      headers: this.createAuthorizationHeader()
    };

    return this.http.post(url, body, options)
        .map((response: Response) => response)
        .catch((error: any) => Observable.throw(error.error || 'Server error'));
  }

  patch(url, body): Observable<any> {
    const options = {
      headers: this.createAuthorizationHeader()
    };

    return this.http.patch(url, body, options)
        .map((response: Response) => response)
        .catch((error: any) => Observable.throw(error.error || 'Server error'));
  }


}
