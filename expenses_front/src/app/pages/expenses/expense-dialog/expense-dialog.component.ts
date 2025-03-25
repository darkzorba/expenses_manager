import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms'; // Para os formulários reativos

@Component({
  selector: 'app-expense-dialog',
  templateUrl: './expense-dialog.component.html',
  styleUrls: ['./expense-dialog.component.css']
})
export class ExpenseDialogComponent {
  expenseForm: FormGroup;  // Formulário reativo para criação da despesa
  types:Array<any> = []
  constructor(
    public dialogRef: MatDialogRef<ExpenseDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, // Recebe os dados do componente pai
    private fb: FormBuilder
  ) {
    // Criação do formulário reativo
    this.expenseForm = this.fb.group({
      value: [null, [Validators.required, Validators.min(0)]],
      description: ['', Validators.required],
      type: ['', Validators.required],
      date_expense: ['', Validators.required]
    });
  }

  // Fechar o modal e enviar os dados
  onNoClick(): void {
    this.dialogRef.close();
  }

  onSave(): void {
    if (this.expenseForm.valid) {
      const newExpense = this.expenseForm.value;
      this.dialogRef.close(newExpense);  // Envia os dados para o componente pai
    }
  }
}
