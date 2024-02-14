pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from Git repository
                git branch: 'dev', url: 'https://github.com/jayanthbillemane/arbicloud'
                echo 'Checked out code successfully'
            }
        }
        stage('Deploy') {
            when {
                branch 'dev' // Only run this stage for the dev branch
            }
            steps {
                // Retrieve the server credential
                withCredentials([string(credentialsId: 'SERVER', variable: 'SERVER')]) {
                    // Use Jenkins credentials to retrieve values securely
                    withCredentials([
                        usernamePassword(credentialsId: '81710b21-7d87-40d1-8e05-6c2a17e9662f', usernameVariable: 'Username', passwordVariable: 'Password'),
                        file(credentialsId: 'pemid', variable: 'PEM_FILE')
                    ]) {

                        // Print credential values (optional)
                        echo "Username: $USERNAME"
                        echo "Username: $SERVER"

                        // Deploy changes to the server
                        // sh "ssh  -o StrictHostKeyChecking=no -i $PEM_FILE $USERNAME@$SERVER 'cd /home/azureuser/arbifrontend && git pull && sudo docker-compose build && sudo docker-compose up -d'"
                        sh "echo '$PASSWORD' | ssh -o StrictHostKeyChecking=no -i $PEM_FILE azureuser@$SERVER 'cd /home/azureuser/arbicloud && git pull && echo \"$PASSWORD\" | sudo -S docker-compose build && sudo -S docker-compose up -d'"

                    }
                }
            }
        }
    }
}
