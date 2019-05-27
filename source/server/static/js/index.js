// ----------------------------------------------------------------------------
// Copyright © Ludovic Ortega, 2019
//
// Contributeur(s):
//     * Ortega Ludovic - mastership@hotmail.fr
//     * Denis Genon-Catalot - denis.genon-catalot@univ-grenoble-alpes.fr
//
// Ce logiciel, PiDashboard, est un programme informatique à but éducatif.
// Il a été developpé spécialement pour des travaux pratiques sur l'IoT et
// des RaspberryPi.
//
// Ce logiciel est régi par la licence CeCILL soumise au droit français et
// respectant les principes de diffusion des logiciels libres. Vous pouvez
// utiliser, modifier et/ou redistribuer ce programme sous les conditions
// de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
// sur le site "http://www.cecill.info".
//
// En contrepartie de l'accessibilité au code source et des droits de copie,
// de modification et de redistribution accordés par cette licence, il n'est
// offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
// seule une responsabilité restreinte pèse sur l'auteur du programme,  le
// titulaire des droits patrimoniaux et les concédants successifs.
//
// A cet égard  l'attention de l'utilisateur est attirée sur les risques
// associés au chargement,  à l'utilisation,  à la modification et/ou au
// développement et à la reproduction du logiciel par l'utilisateur étant
// donné sa spécificité de logiciel libre, qui peut le rendre complexe à
// manipuler et qui le réserve donc à des développeurs et des professionnels
// avertis possédant  des  connaissances  informatiques approfondies.  Les
// utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
// logiciel à leurs besoins dans des conditions permettant d'assurer la
// sécurité de leurs systèmes et ou de leurs données et, plus généralement,
// à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
//
// Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
// pris connaissance de la licence CeCILL, et que vous en avez accepté les
// termes.
// ----------------------------------------------------------------------------

'use strict';

let informations = [];
informations["refresh"] = 1;

document.addEventListener('DOMContentLoaded', () => {
    /////////////////////////////
    ////////INFORMATIONS/////////
    /////////////////////////////
    let informations_health = document.getElementById("informations-health");
    let informations_uptime = document.getElementById("informations-uptime");
    let informations_refresh = document.getElementById("informations-refresh");
    let informations_phone = document.getElementById("informations-phone");

    get_informations();
    setInterval(get_informations,1000);

    function get_informations() {
        fetch('/get/information').then(function(response) {
            return (response.json());
        })
        .then(function(data)
        {
            informations = data;
            if(informations_health.innerHTML !== data["health"])
            {
                if(data["health"] === "DOWN")
                {
                    change_status(informations_health, data["health"], "is-success", "is-danger");
                }
                else
                {
                    change_status(informations_health, data["health"], "is-danger", "is-success");
                }
            }
            if(informations_uptime.innerHTML !== data["uptime"])
            {
                if(data["uptime"] === "UNKNOW")
                {
                    change_status(informations_uptime, data["uptime"], "is-info", "is-danger");
                }
                else
                {
                    change_status(informations_uptime, data["uptime"], "is-danger", "is-info");
                }
            }

            if(informations_refresh.innerHTML !== data["refresh"])
            {
                change_status(informations_refresh, data["refresh"] + 's', "is-danger", "is-info");
            }

            if(informations_phone.innerHTML !== data["phone_number"])
            {
                change_status(informations_phone, data["phone_number"], "is-danger", "is-info");
            }
        })
        .catch(function(error)
        {
            console.log('Fetch API error: ' + error.message);

            const text_error = "ERROR";
            const class_error = "is-danger";

            change_status(informations_health, text_error, "is-success", class_error);
            change_status(informations_uptime, text_error, "is-info", class_error);
            change_status(informations_refresh, text_error, "is-info", class_error);
            change_status(informations_phone, text_error, "is-info", class_error);
        });
    }

    function change_status(el, html, classToRemove, classToAdd)
    {
        el.innerHTML = html;
        if(el.classList.contains(classToRemove)) {el.classList.remove(classToRemove);}
        if(!el.classList.contains(classToAdd)) {el.classList.add(classToAdd);}
    }

    /////////////////////////////
    //////////////LED////////////
    /////////////////////////////

    let led = document.getElementById('led');
    let errorLed = document.getElementById('error-led');

    get_led();
    setInterval(get_led, 1000 * informations["refresh"]);

    function get_led() {
        fetch('/get/data/led').then(function(response) {
            return (response.json());
        })
        .then(function(data)
        {
            if(led.classList.contains("is-hidden"))
            {
                led.classList.remove("is-hidden")
            }

            if(!errorLed.classList.contains("is-hidden"))
            {
                errorLed.classList.add("is-hidden")
            }

            for(let key in data) {
                let led_element = document.getElementById("led_" + key);
                if(!led_element)
                {
                    let column_led = Object.keys(data).length % 2 !== 0 ? "led_column_left" : "led_column_right";
                    let color_led = data[key] === "ON" ? "is-success" : "is-danger";
                    let add_led = '<div id="led_' + key + '" class="notification ' + color_led + '">\n<span class="icon is-small"><i class="fas fa-lightbulb"></i></span>&nbsp;<strong>' + key + '</strong>\n</div>';
                    document.getElementById(column_led).insertAdjacentHTML('beforeend', add_led);
                }
                else
                {
                    if(data[key] === "ON")
                    {
                        if(led_element.classList.contains("is-danger"))
                        {
                            led_element.classList.remove("is-danger")
                        }

                        if(!led_element.classList.contains("is-success"))
                        {
                            led_element.classList.add("is-success")
                        }
                    }
                    else
                    {
                        if(led_element.classList.contains("is-success"))
                        {
                            led_element.classList.remove("is-success")
                        }

                        if(!led_element.classList.contains("is-danger"))
                        {
                            led_element.classList.add("is-danger")
                        }
                    }
                }

            }

        })
        .catch(function(error)
        {
            console.log('Fetch API error: ' + error.message);

            if(!led.classList.contains("is-hidden"))
            {
                led.classList.add("is-hidden")
            }

            if(errorLed.classList.contains("is-hidden"))
            {
                errorLed.classList.remove("is-hidden")
            }
        });
    }

    /////////////////////////////
    ////////TEMPERATURE//////////
    /////////////////////////////

    let temperature = document.getElementById('temperature');
    let errorTemperature = document.getElementById('error-temperature');

    let data = {
        labels: [],
        datasets: [{
            label: 'RaspberryPi temperature',
            data: [],
            backgroundColor: 'rgba(253, 108, 158, 0.2)',
            borderColor: 'rgba(253, 108, 158, 1)',
            borderWidth: 1
        }]
    };

    let options = {
        responsive: true,
        scales: {
            xAxes: [{
                type: "time",
                distribution: "series",
                time: {
                    unit: "minute"
                },
                scaleLabel: {
                    display: true,
                    labelString: "Time"
                }
            }],
            yAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: "Temperature (°C)"
                },
                ticks: {
                    min: -20,
                    max: 50,
                    stepSize: 5
                },
                stacked: true
            }]
        }
    };

    let TemperatureChart = new Chart(temperature, {
        type: 'line',
        data: data,
        options: options
    });

    get_temperature();
    setInterval(get_temperature, 1000 * informations["refresh"]);

    function get_temperature() {
        fetch('/get/data/temperature').then(function(response) {
            return (response.json());
        })
        .then(function(data)
        {
            if(temperature.classList.contains("is-hidden"))
            {
                temperature.classList.remove("is-hidden")
            }

            if(!errorTemperature.classList.contains("is-hidden"))
            {
                errorTemperature.classList.add("is-hidden")
            }

            TemperatureChart.data.labels = (data["datetime"].map(date => new Date(date).toLocaleString("en-EN")));
            TemperatureChart.data.datasets.forEach((dataset) => {
                dataset.data = data["value"];
            });
            TemperatureChart.update();
        })
        .catch(function(error)
        {
            console.log('Fetch API error: ' + error.message);

            if(!temperature.classList.contains("is-hidden"))
            {
                temperature.classList.add("is-hidden")
            }

            if(errorTemperature.classList.contains("is-hidden"))
            {
                errorTemperature.classList.remove("is-hidden")
            }
        });
    }
});