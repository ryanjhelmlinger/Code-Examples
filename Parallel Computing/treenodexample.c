


#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode
{
	char symbol;
	int frequency;

	struct Node* left;
	struct Node* right;
};

int main(int argv, char* argv[])
{
	TreeNode t = NULL;

	t = (TreeNode*)malloc(sizeOf(TreeNode));

	(*t).symbol = 'A';
	//or
	t -> frequency = 7;

	t.symbol = 'a';
	t.frequency = 7;

	printf("%c\n", t.symbol);
	printf("%i\n", t.frequency);

	return 0;

}