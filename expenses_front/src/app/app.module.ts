import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {ButtonModule} from "primeng/button";
import {TableModule} from "primeng/table";
import { ExpensesComponent } from './pages/expenses/expenses.component';
import {DialogModule} from "primeng/dialog";
import {MatTableModule} from "@angular/material/table";
import {MatPaginatorModule} from "@angular/material/paginator";
import {MatButtonModule} from "@angular/material/button";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import { ExpenseDialogComponent } from './pages/expenses/expense-dialog/expense-dialog.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {MatDialogModule} from "@angular/material/dialog";
import {MatInputModule} from "@angular/material/input";
import {ReactiveFormsModule} from "@angular/forms";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatNativeDateModule} from "@angular/material/core";

@NgModule({
  declarations: [
    AppComponent,
    ExpensesComponent,
    ExpenseDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatPaginatorModule,
    MatButtonModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatDialogModule,
    MatInputModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
