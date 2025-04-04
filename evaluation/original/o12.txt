#include <semaphore.h>
#define NUM_CUSTOMERS 20
#define NUM_OPERATORS 4

int customersLeft = NUM_CUSTOMERS;
sem_t line_num_lock;
int line_num = 0;
// sem_t available_operators;
sem_t customers[NUM_CUSTOMERS];
sem_t operators[NUM_OPERATORS];
int customer2operator[NUM_CUSTOMERS];
int answers[NUM_CUSTOMERS];
sem_t cust_num_lock;
int cust_num = 0;


void Customer() {
	//TODO: რიგში ჩადგომა და ლოდინი სანამ რომელიმე ოპერატორი გამოიძახებს
    sem_wait(&line_num_lock);
    int id = line_num;
    line_num++;
    sem_post(&line_num_lock);
    sem_wait(customers+id);
    int o_id = customer2operator[id];

	fillApplication();
	//TODO: ელოდება სანამ ოპერატორი გადაამოწმებს მონაცემებს
    sem_post(operators+ o_id);
    sem_wait(customers+id);
	//TODO: ბეჭდავს პასუხს(Yes/No)
    if (answers[id]) 
        printf("YES\n");
    else
        printf("NO\n");
}

void Operator(void * data) {
	int my_id = data->id;
	int succeful_applications = 0;
	while (1) {
		//TODO: ელოდება სანამ მომხმარებელი ჩადგება რიგში
		//TODO: მომხმარებლის გამოძახება და ლოდინი სანამ მომხმარებელი შეავსებს ფორმას
        sem_wait(&cust_num_lock);
		if (customersLeft == 0) {
			sem_post(&cust_num_lock);
			break;
		}
        int cust_id = cust_num;
        cust_num++;
		customersLeft--;
        sem_post(&cust_num_lock);

		customer2operator[cust_id] = my_id;
        sem_post(customers+cust_id);
        sem_wait(operators+my_id);
        
		int res = checkApplication();//აბრუნებს შედეგს - 1 თანხმობა, 0 უარყოფა 
		//TODO: მომხმარებლისთვის პასუხის დაბრუნება
		answers[cust_id] = res;
        sem_post(customers+cust_id);
		succeful_applications += res;
	}
	//TODO: ბეჭდავს მის მიერ დამტკიცებული სესხების რაოდენობიის
	printf("successful applications %d\n", succeful_applications);
}

int main() {
	//მომხმარებლების ნაკადების გაშვება
	for (int i=0; i<NUM_CUSTOMERS; i++) {
		pthread_t * t = malloc(sizeof(pthread_t));
		pthread_create(t, NULL, Customer, NULL);
	}

	//ოპერატორების ნაკადების გაშვება
	for (int i=0; i<NUM_OPERATORS; i++) {
		pthread_t * t = malloc(sizeof(pthread_t));
		pthread_create(t, NULL, Operator, NULL);
	}

	pthread_exit(0);
}