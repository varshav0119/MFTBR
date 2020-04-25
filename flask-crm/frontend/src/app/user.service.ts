import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


import { User } from './user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  userUrl: "localhost:5000/users"

  constructor(private http: HttpClient) { }
  
  getUsers() {
    console.warn("users");
    let userList = this.http.get(this.userUrl);
    console.warn(userList);
    return userList;
  }
}
