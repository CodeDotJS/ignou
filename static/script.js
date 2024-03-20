    document.addEventListener('DOMContentLoaded', function() {
        const currentYear = new Date().getFullYear();
        const selectElement = document.getElementById("year");

        for (let year = currentYear; year >= 2018; year--) {
            const option = document.createElement("option");
            option.value = year.toString().slice(-2);
            option.textContent = year;
            selectElement.appendChild(option);
        }

        window.onload = function() {
            const savedData = localStorage.getItem('fetchedData');
            if (savedData) {
                document.getElementById('resultContainer').innerHTML = savedData;
                document.getElementById('fetchForm').style.display = 'none';
                document.getElementById('deleteBtn').style.display = 'inline-block';
            } else {
                document.getElementById('deleteBtn').style.display = 'none';
                document.getElementById('refreshBtn').style.display = 'none';
            }

            const savedMonth = localStorage.getItem('savedMonth');
            const savedYear = localStorage.getItem('savedYear');
            const savedEnrollment = localStorage.getItem('savedEnrollment');

            if (savedEnrollment) {
                document.getElementById('enrollment').value = savedEnrollment;
                document.getElementsByTagName('select')[0].selectedIndex = savedMonth;
                document.getElementsByTagName('select')[1].selectedIndex = savedYear;
            }

            document.getElementById('last').innerText = localStorage.getItem('lastChecked');
            document.getElementById('message').style.display = 'none';
        };

        document.getElementById('fetchForm').addEventListener('submit', async function(event) {
            event.preventDefault();
            try {
                document.getElementById('loader').style.display = 'block'; // Show loader
                const formData = new FormData(this);
                const response = await fetch('/fetch_data', {
                    method: 'POST',
                    body: formData
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const data = await response.text();
                document.getElementById('resultContainer').innerHTML = data;
                localStorage.setItem('fetchedData', data);
                document.getElementById('deleteBtn').style.display = 'inline-block';

                localStorage.setItem('savedEnrollment', formData.get('enrollment'));
                document.getElementById('fetchForm').style.display = 'none';
                document.getElementById('refreshBtn').style.display = 'inline-block';
                document.getElementById('message').style.display = 'none';

                const month = document.getElementsByTagName('select')[0].selectedIndex;
                const year = document.getElementsByTagName('select')[1].selectedIndex;
                localStorage.setItem('savedMonth', month);
                localStorage.setItem('savedYear', year);

                const timestamp = new Date().toLocaleString();
                localStorage.setItem('lastChecked', timestamp);
            } catch (error) {
                console.error('Error fetching data:', error.message);
            } finally {
                document.getElementById('loader').style.display = 'none';
            }
        });

        document.getElementById('refreshBtn').addEventListener('click', async function() {
            try {
                document.getElementById('loader').style.display = 'block';
                const formData = new FormData(document.getElementById('fetchForm'));
                const response = await fetch('/fetch_data', {
                    method: 'POST',
                    body: formData
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const newData = await response.text();
                const savedData = localStorage.getItem('fetchedData');

                if (newData !== savedData) {
                    document.getElementById('resultContainer').innerHTML = newData;
                    localStorage.setItem('fetchedData', newData);
                } else {
                    document.getElementById('statusContainer').innerText = 'There\'s no new result available. Come back soon!';
                }
                const timestamp = new Date().toLocaleString();
                localStorage.setItem('lastChecked', timestamp);
                document.getElementById('last').innerText = 'Just Now';
            } catch (error) {
                console.error('Error refreshing data:', error.message);
            } finally {
                document.getElementById('loader').style.display = 'none';
            }
        });

        document.getElementById('deleteBtn').addEventListener('click', function() {
            localStorage.removeItem('fetchedData');
            document.getElementById('resultContainer').innerHTML = '';
            document.getElementById('fetchForm').style.display = 'block';
            document.getElementById('deleteBtn').style.display = 'none';
            document.getElementById('refreshBtn').style.display = 'none';
            document.getElementById('message').style.display = 'inline-block';
            document.getElementById('statusContainer').innerText = '';
        });
    });
