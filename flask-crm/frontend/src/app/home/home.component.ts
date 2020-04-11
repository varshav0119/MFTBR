import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { UserList } from '../user_list';
import { ProductList } from '../product_list';
import { RCombination } from '../rc';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  form1 = new FormGroup({
    iduser: new FormControl('', [this.validUserValidator]), 
    idproduct: new FormControl('', [this.validProductValidator])
  });

  form2 = new FormGroup({
    iduser: new FormControl(''),
    idproduct: new FormControl('')
  })

  rcList: RCombination[];
  rcUrl: string;
  
  constructor(private http: HttpClient) { 
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
    console.warn(this.form1.value);
    // this.predict(this.form1.get('iduser').value, this.form.get('idproduct').value)

  }

  onSubmit2(){
    console.warn(this.form2.value);
  }

  predict(iduser: number, idproduct: number){
    // let params = new HttpParams().set('iduser',String(iduser)).set('idproduct',String(idproduct));
    // this.http.get<any>('http://localhost:5000/model', {params}).subscribe( data => { this.response = data})
    // this.modelService.getModel(iduser, idproduct)
    //         .subscribe((data: any) => this.response = data);
    
  }

}
