import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog } from '@angular/material/dialog';  // Importar MatDialog para modais
import { ExpensesService } from './expenses.service'; // Serviço para pegar dados
import { ExpenseDialogComponent } from './expense-dialog/expense-dialog.component'; // Componente do modal

interface Expense {
  value: number;
  name: string;
  description: string;
  date_expense: string;
  expense_percent: number;
  income_percent: number;
}

@Component({
  selector: 'app-expenses',
  templateUrl: './expenses.component.html',
  styleUrls: ['./expenses.component.css']
})
export class ExpensesComponent implements OnInit,AfterViewInit {
  displayedColumns: string[] = ['value', 'description', 'date_expense', 'expense_percent', 'income_percent'];
  totalExpenseValue: number = 1000;
  totalIncomeValue: number = 2000;
  dataSource = new MatTableDataSource<Expense>([]);
  expenses: Expense[] = [];
  dateOptions: string[] = [];  // Variável para armazenar as opções de datas

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private expenseService: ExpensesService,
    private dialog: MatDialog // Injete o MatDialog
  ) {}

  ngOnInit(): void {
    this.getExpenses();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
  }

  // Método para abrir o modal
  openExpenseDialog(): void {
    const dialogRef = this.dialog.open(ExpenseDialogComponent, {
      width: '400px',
      data: {
        dateOptions: this.dateOptions  // Envia as opções de data para o modal
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Adiciona o novo expense à lista
        this.expenses.push(result);
        this.dataSource.data = [...this.expenses];  // Atualiza a tabela
      }
    });
  }

  // Método para obter as despesas e as datas disponíveis
  getExpenses(): void {
    this.expenseService.getExpensesByMonth('3').subscribe(
      (data) => {
        this.expenses = data.expenses.list_expenses;
        this.totalExpenseValue = data.expenses.total_expenses;
        this.totalIncomeValue = data.expenses.total_income;
        this.dateOptions = data.expenses.date_options;  // Recebe as opções de data do backend
        this.dataSource.data = this.expenses;
      },
      (error) => {
        console.error('Erro ao obter despesas:', error);
      }
    );
  }
}
