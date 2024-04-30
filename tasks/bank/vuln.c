#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAX_ACCOUNTS 10

// Define the structure for an account
typedef struct
{
    int accountNumber;
    char ownerName[64];
    long int balance;
} BankAccount;

void win()
{
    execve("/bin/sh", NULL, NULL);
}

// Function to create a new account
BankAccount *createAccount(const char *ownerName, long initialBalance)
{
    BankAccount *newAccount = (BankAccount *)calloc(1, sizeof(BankAccount));

    if (newAccount == NULL)
    {
        printf("Memory allocation failed.\n");
        exit(1);
    }

    // Generate a random account number
    newAccount->accountNumber = rand() % 10000 + 1000;

    strncpy(newAccount->ownerName, ownerName, sizeof(newAccount->ownerName) - 1);
    newAccount->balance = initialBalance;

    return newAccount;
}

// Function to find an account based on its account number
BankAccount *findAccount(int accountNumber, BankAccount accounts[])
{
    for (int i = 0;; ++i)
    {
        if (accounts[i].accountNumber == accountNumber)
        {
            return &accounts[i];
        }
    }
    return NULL;
}

// Function to transfer money between two accounts
void transferMoney(BankAccount *sender, BankAccount *receiver, long amount)
{
    if (sender->balance >= amount)
    {
        sender->balance -= amount;
        receiver->balance += amount;
        printf("Transfer successful.\n");
    }
    else
    {
        printf("Insufficient funds.\n");
    }
}

// Function to check the account balance
void checkBalance(BankAccount *account)
{
    printf("Account Number: %d\n", account->accountNumber);
    printf("Owner Name: %s\n", account->ownerName);
    printf("Balance: %ld\n", account->balance);
}

int bank()
{
    // Declare an array to store accounts
    BankAccount accounts[MAX_ACCOUNTS];
    int numAccounts = 0;

    // CLI loop
    while (1)
    {
        // Display menu
        printf("\nMenu:\n");
        printf("1. Create Account\n");
        printf("2. Check Balance\n");
        printf("3. Transfer Money\n");
        printf("4. Exit\n");

        // Get user choice
        printf("Enter your choice: ");
        int option;
        scanf("%d", &option);

        switch (option)
        {
        case 1:
            // Create Account
            printf("Enter Owner Name: ");
            char ownerName[84];
            fgets(ownerName, sizeof(ownerName), stdin);
            printf("Enter Initial Balance: ");
            long initialBalance;
            scanf("%ld", &initialBalance);

            // Create the account and add it to the array
            if (numAccounts < MAX_ACCOUNTS)
            {
                BankAccount *tmp_account = createAccount(ownerName, initialBalance);
                BankAccount *account = &accounts[numAccounts++];

                memcpy(account, tmp_account, sizeof(BankAccount));
                free(tmp_account);

                printf("Account created successfully.\n");
                checkBalance(account);
            }
            else
            {
                printf("Maximum number of accounts reached.\n");
            }
            break;

        case 2:
            // Check Balance
            printf("Enter Account Number: ");
            int accountNumber;
            scanf("%d", &accountNumber);

            // Find the account and display the balance
            BankAccount *account = findAccount(accountNumber, accounts);
            if (account != NULL)
            {
                checkBalance(account);
            }
            else
            {
                printf("Account not found.\n");
            }
            break;

        case 3:
            // Transfer Money
            printf("Enter Sender Account Number: ");
            scanf("%d", &accountNumber);

            // Find the sender account
            BankAccount *sender = findAccount(accountNumber, accounts);
            if (sender == NULL)
            {
                printf("Sender account not found.\n");
                break;
            }

            printf("Enter Receiver Account Number: ");
            scanf("%d", &accountNumber);

            // Find the receiver account
            BankAccount *receiver = findAccount(accountNumber, accounts);
            if (receiver == NULL)
            {
                printf("Receiver account not found.\n");
                break;
            }

            printf("Enter Transfer Amount: ");
            long transferAmount;
            scanf("%ld", &transferAmount);

            // Transfer money between accounts
            transferMoney(sender, receiver, transferAmount);

            // Display updated balances
            printf("Updated Balances\n");
            break;

        case 4:
            // Exit the program
            printf("Exiting the program.\n");
            return 0;

        default:
            printf("Invalid option. Please try again.\n");
        }
    }

    return 0;
}

int main()
{
    setbuf(stdout, NULL);
    // Seed the random number generator with the current time
    srand((unsigned int)time(NULL));

    bank();

    return 0;
}