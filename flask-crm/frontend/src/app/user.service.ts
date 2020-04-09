import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


import { User } from './user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  userUrl: "localhost:5000/user"

  constructor(private http: HttpClient) { }
  getUsers() {
    return this.http.get<User[]>(this.userUrl);
  }
}
