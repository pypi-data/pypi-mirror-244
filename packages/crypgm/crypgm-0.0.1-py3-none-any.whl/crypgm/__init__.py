def p1():
    return """#include <stdio.h>

// Function to perform Caesar Cipher encryption
void encryptMessage(char message[], int key) {
    int i;
    char ch;

    for (i = 0; message[i] != '\0'; ++i) {
        ch = message[i];

        // Encrypt uppercase letters
        if (ch >= 'A' && ch <= 'Z') {
            message[i] = (ch + key - 'A') % 26 + 'A';
        }
        // Encrypt lowercase letters
        else if (ch >= 'a' && ch <= 'z') {
            message[i] = (ch + key - 'a') % 26 + 'a';
        }
    }
}

int main() {
    char message[100];
    int key;

    // Input the message from the user
    printf("Enter a message: ");
    fgets(message, sizeof(message), stdin);

    // Input the key for encryption
    printf("Enter the key (an integer): ");
    scanf("%d", &key);

    // Call the function to encrypt the message
    encryptMessage(message, key);

    // Display the encrypted message
    printf("Encrypted message: %s\n", message);

    return 0;
}

"""

def p2():
    return """#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define SIZE 5

// Function to generate the Playfair key table
void generateKeyTable(char key[], char keyTable[][SIZE]) {
    int i, j, k, len;
    char unique_chars[26] = {0};

    len = strlen(key);
    
    // Initialize the key table with the unique characters of the key
    k = 0;
    for (i = 0; i < len; ++i) {
        if (key[i] != ' ' && unique_chars[key[i] - 'A'] == 0) {
            unique_chars[key[i] - 'A'] = 1;
            keyTable[k / SIZE][k % SIZE] = toupper(key[i]);
            ++k;
        }
    }

    // Fill the remaining cells with the remaining unique characters
    for (i = 0; i < 26; ++i) {
        if (unique_chars[i] == 0 && i != ('J' - 'A')) {
            keyTable[k / SIZE][k % SIZE] = 'A' + i;
            ++k;
        }
    }
}

// Function to find the positions of two characters in the key table
void findPosition(char keyTable[][SIZE], char ch, int *row, int *col) {
    int i, j;
    for (i = 0; i < SIZE; ++i) {
        for (j = 0; j < SIZE; ++j) {
            if (keyTable[i][j] == ch) {
                *row = i;
                *col = j;
                return;
            }
        }
    }
}

// Function to perform Playfair Cipher encryption
void encryptMessage(char message[], char keyTable[][SIZE]) {
    int i, row1, col1, row2, col2;
    char ch1, ch2;

    for (i = 0; message[i] != '\0'; i += 2) {
        ch1 = toupper(message[i]);
        ch2 = (message[i + 1] == '\0') ? 'X' : toupper(message[i + 1]);

        // Find positions of the characters in the key table
        findPosition(keyTable, ch1, &row1, &col1);
        findPosition(keyTable, ch2, &row2, &col2);

        // Encrypt the characters based on the rules of the Playfair Cipher
        if (row1 == row2) {
            // Same row, shift columns
            message[i] = keyTable[row1][(col1 + 1) % SIZE];
            message[i + 1] = keyTable[row2][(col2 + 1) % SIZE];
        } else if (col1 == col2) {
            // Same column, shift rows
            message[i] = keyTable[(row1 + 1) % SIZE][col1];
            message[i + 1] = keyTable[(row2 + 1) % SIZE][col2];
        } else {
            // Different row and column, form a rectangle
            message[i] = keyTable[row1][col2];
            message[i + 1] = keyTable[row2][col1];
        }
    }
}

int main() {
    char key[50], message[100], keyTable[SIZE][SIZE];

    // Input the key from the user
    printf("Enter the key (no spaces): ");
    scanf("%s", key);

    // Generate the key table
    generateKeyTable(key, keyTable);

    // Input the message from the user
    printf("Enter the message to be encrypted: ");
    scanf("%s", message);

    // Call the function to encrypt the message
    encryptMessage(message, keyTable);

    // Display the encrypted message
    printf("Encrypted message: %s\n", message);

    return 0;
}

"""

def p3():
    return """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX_SIZE 10

// Function to calculate the determinant of a 2x2 matrix
int calculateDeterminant(int matrix[2][2]) {
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
}

// Function to calculate the inverse of a 2x2 matrix
void calculateInverse(int matrix[2][2], int inverse[2][2]) {
    int det = calculateDeterminant(matrix);

    if (det != 0) {
        int temp = matrix[0][0];
        matrix[0][0] = matrix[1][1];
        matrix[1][1] = temp;

        matrix[0][1] = -matrix[0][1];
        matrix[1][0] = -matrix[1][0];

        for (int i = 0; i < 2; ++i) {
            for (int j = 0; j < 2; ++j) {
                inverse[i][j] = matrix[i][j] / det;
            }
        }
    } else {
        printf("Matrix is not invertible.\n");
        exit(EXIT_FAILURE);
    }
}

// Function to encrypt a message using Hill Cipher
void encryptMessage(char message[], int keyMatrix[2][2]) {
    int len = strlen(message);

    // Check if the length of the message is even
    if (len % 2 != 0) {
        printf("The length of the message should be even.\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < len; i += 2) {
        // Convert characters to uppercase
        int char1 = toupper(message[i]) - 'A';
        int char2 = toupper(message[i + 1]) - 'A';

        // Create a message vector
        int messageVector[2] = {char1, char2};

        // Perform matrix multiplication with the key matrix
        int resultVector[2] = {
            keyMatrix[0][0] * messageVector[0] + keyMatrix[0][1] * messageVector[1],
            keyMatrix[1][0] * messageVector[0] + keyMatrix[1][1] * messageVector[1]
        };

        // Apply modulo 26 to keep the result within the range of the alphabet
        for (int j = 0; j < 2; ++j) {
            resultVector[j] = (resultVector[j] + 26) % 26;
        }

        // Convert back to uppercase letters
        message[i] = resultVector[0] + 'A';
        message[i + 1] = resultVector[1] + 'A';
    }
}

int main() {
    char message[MAX_SIZE];
    int keyMatrix[2][2];
    int inverseMatrix[2][2];

    // Input the key matrix from the user
    printf("Enter the 2x2 key matrix (space-separated values, row by row):\n");
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            scanf("%d", &keyMatrix[i][j]);
        }
    }

    // Calculate the inverse of the key matrix
    calculateInverse(keyMatrix, inverseMatrix);

    // Input the message from the user
    printf("Enter the message to be encrypted (uppercase, no spaces): ");
    scanf("%s", message);

    // Call the function to encrypt the message
    encryptMessage(message, keyMatrix);

    // Display the encrypted message
    printf("Encrypted message: %s\n", message);

    return 0;
}

"""

def p4():
    return """#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function to perform Vigenere Cipher encryption
void encryptVigenere(char message[], char key[]) {
    int messageLength = strlen(message);
    int keyLength = strlen(key);

    // Repeat the key to match the length of the message
    char repeatedKey[messageLength];
    for (int i = 0, j = 0; i < messageLength; ++i, ++j) {
        if (j == keyLength) {
            j = 0;
        }
        repeatedKey[i] = toupper(key[j]);
    }

    // Encrypt the message using the Vigenere Cipher
    for (int i = 0; i < messageLength; ++i) {
        if (isalpha(message[i])) {
            char base = isupper(message[i]) ? 'A' : 'a';
            message[i] = (message[i] - base + repeatedKey[i] - 'A') % 26 + base;
        }
    }
}

int main() {
    char message[100], key[100];

    // Input the message from the user
    printf("Enter the message to be encrypted: ");
    fgets(message, sizeof(message), stdin);

    // Input the key from the user
    printf("Enter the key: ");
    fgets(key, sizeof(key), stdin);

    // Call the function to encrypt the message
    encryptVigenere(message, key);

    // Display the encrypted message
    printf("Encrypted message: %s\n", message);

    return 0;
}

"""

def p5():
    return """#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function to perform Rail Fence Cipher encryption (row-wise)
void encryptRowWise(char message[], int rails, char encryptedMessage[]) {
    int len = strlen(message);
    int railGrid[rails][len];

    // Initialize the rail grid
    for (int i = 0; i < rails; ++i) {
        for (int j = 0; j < len; ++j) {
            railGrid[i][j] = 0;
        }
    }

    // Fill the rail grid with the message
    int row = 0;
    int direction = 1; // 1 for down, -1 for up

    for (int i = 0; i < len; ++i) {
        railGrid[row][i] = message[i];

        if (row == 0) {
            direction = 1; // Change direction when reaching the top rail
        } else if (row == rails - 1) {
            direction = -1; // Change direction when reaching the bottom rail
        }

        row += direction;
    }

    // Read the rail grid to get the encrypted message
    int index = 0;
    for (int i = 0; i < rails; ++i) {
        for (int j = 0; j < len; ++j) {
            if (railGrid[i][j] != 0) {
                encryptedMessage[index++] = railGrid[i][j];
            }
        }
    }
    encryptedMessage[index] = '\0';
}

// Function to perform Rail Fence Cipher encryption (column-wise)
void encryptColumnWise(char message[], int rails, char encryptedMessage[]) {
    int len = strlen(message);
    int railGrid[rails][len];

    // Initialize the rail grid
    for (int i = 0; i < rails; ++i) {
        for (int j = 0; j < len; ++j) {
            railGrid[i][j] = 0;
        }
    }

    // Fill the rail grid with the message
    int col = 0;
    int direction = 1; // 1 for right, -1 for left

    for (int i = 0; i < len; ++i) {
        railGrid[col][i] = message[i];

        if (col == 0) {
            direction = 1; // Change direction when reaching the leftmost rail
        } else if (col == rails - 1) {
            direction = -1; // Change direction when reaching the rightmost rail
        }

        col += direction;
    }

    // Read the rail grid to get the encrypted message
    int index = 0;
    for (int i = 0; i < rails; ++i) {
        for (int j = 0; j < len; ++j) {
            if (railGrid[i][j] != 0) {
                encryptedMessage[index++] = railGrid[i][j];
            }
        }
    }
    encryptedMessage[index] = '\0';
}

int main() {
    char message[100], encryptedRowWise[100], encryptedColumnWise[100];
    int rails;

    // Input the message from the user
    printf("Enter the message to be encrypted: ");
    fgets(message, sizeof(message), stdin);

    // Input the number of rails from the user
    printf("Enter the number of rails: ");
    scanf("%d", &rails);

    // Call the function to encrypt the message (row-wise)
    encryptRowWise(message, rails, encryptedRowWise);

    // Call the function to encrypt the message (column-wise)
    encryptColumnWise(message, rails, encryptedColumnWise);

    // Display the encrypted messages
    printf("Encrypted message (Row-wise): %s\n", encryptedRowWise);
    printf("Encrypted message (Column-wise): %s\n", encryptedColumnWise);

    return 0;
}

"""
