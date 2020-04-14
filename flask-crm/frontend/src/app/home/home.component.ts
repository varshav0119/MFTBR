import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { UserList } from '../user_list';
import { ProductList } from '../product_list';
import { RCombination } from '../rc';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  form1 = new FormGroup({
    iduser: new FormControl('', [this.validUserValidator]),
    idproduct: new FormControl('', [this.validProductValidator])
  }) 

  form2 = new FormGroup({
    iduser_and_product: new FormControl('')
  })

  rcList: RCombination[];
  rcUrl: string;
  
  constructor(private http: HttpClient, private router: Router) { 
    this.rcUrl = "http://localhost:5000/reviewed_combinations/safe";
  }

  ngOnInit(): void {
    this.http.get<RCombination[]>(this.rcUrl).subscribe( data => { this.rcList = data});
  }

  validProductValidator(control: FormControl): any {
    let p = control.value;
    for (let product of ProductList)
    {
      if(product == p)
        return null;
    }
    return  {'validUser': {value: control.value}};
  }

  validUserValidator(control: FormControl): any {
    let u = control.value;
    for (let user of UserList)
    {
      if(user == u)
        return null;
    }
    return  {'validUser': {value: control.value}};
  }

  onSubmit1(){
    this.router.navigate(['model', {iduser: this.form1.get('iduser').value, idproduct: this.form1.get('idproduct').value}])

  }

  onSubmit2(){
    this.router.navigate(['model', this.form2.get('iduser_and_product').value])
  }

}
