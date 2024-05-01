describe('R8 Tests', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let email // email of the user

    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
            .then((user) => {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    uid = response.body._id.$oid
                    email = user.email
                })
            })
        
    })

    beforeEach(function () {
        // enter the main main page and login
        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()
    })

    it('R8UC1 Case 1: User enters a description', () => {
        cy.contains('div', 'Title')
            .find('input[type=text]')
            .type('Sample Task')
        cy.contains('div', 'YouTube URL')
            .find('input[type=text]')
            .type('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        cy.get('form')
            .submit()

        cy.contains('a', 'Sample Task')
            .click();
        
        cy.get('form.inline-form input[type=text]')
            .type('Sample Todo');
        
            
        cy.contains('input', 'Add')
        .should('be.enabled');
    })

    it('R8UC1 Case 2: User enters empty description', () => {
        cy.contains('a', 'Sample Task')
            .click();
        
        cy.contains('input', 'Add')
                .should('be.disabled');

        
    });

    it('R8UC1 Case 3: User clicks "Add" button', () => {
        
        cy.contains('a', 'Sample Task')
            .click();
        
    cy.get('form.inline-form')
            .find('input[type=text]')
            .type('Sample Todo');

        cy.contains('input', 'Add')
            .click();

        cy.get('li.todo-item')
        .should('contain.text', 'Sample Todo')
    });
    
    it('R8UC2 Case 1: User clicks on icon for active todo item', () => {
        cy.contains('a', 'Sample Task')
            .click();
        cy.contains('li.todo-item', 'Sample Todo')
            .find('span.checker')
            .should('have.class', 'unchecked')
            .click();
            cy.contains('li.todo-item', 'Sample Todo')
                .find('span.checker')
                .should('have.class', 'checked')
            
    })

    it('R8UC2 Case 2: User clicks on icon for done todo item', () => {
        cy.contains('a', 'Sample Task')
            .click();
            cy.contains('li.todo-item', 'Sample Todo')
                .find('span.checker')
                .should('have.class', 'checked')
                .click();
                cy.contains('li.todo-item', 'Sample Todo')
                    .find('span.checker')
                    .should('have.class', 'unchecked')
    })
    
    it('R8UC3 Case 1: User clicks on "x" for todo item', () => {
        cy.contains('a', 'Sample Task')
            .click();
        cy.contains('li.todo-item', 'Sample Todo')
            .find('span.remover')
            .click();
            cy.contains('li.todo-item', 'Sample Todo')
                .should('not.exist')
    })

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    });
});
