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

//Navbar
document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0)
    {

        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }

    // Modals
    let rootEl = document.documentElement;
    let $modals = getAll('.modal');
    let $modalButtons = getAll('.modal-button');
    let $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');

    if ($modalButtons.length > 0)
    {
        $modalButtons.forEach(function ($el) {
            $el.addEventListener('click', function () {
                let target = $el.dataset.target;
                let $target = document.getElementById(target);
                rootEl.classList.add('is-clipped');
                $target.classList.add('is-active');
            });
        });
    }

    if ($modalCloses.length > 0) {
        $modalCloses.forEach(function ($el) {
            $el.addEventListener('click', function () {
                closeModals();
            });
        });
    }

    document.addEventListener('keydown', function (event) {
        let e = event || window.event;
        if (e.keyCode === 27)
        {
            closeModals();
        }
    });

    function closeModals()
    {
        rootEl.classList.remove('is-clipped');
        $modals.forEach(function ($el) {
            $el.classList.remove('is-active');
        });
    }

    function getAll(selector)
	{
        return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    if (tabs === undefined) return;

    tabs.forEach((tab) => {
        tab.addEventListener('click', (e) => {
            const tabName = e.currentTarget.id;
            const currentTab = document.querySelector('.tab.is-active');
            const currentContent = document.getElementById(`${currentTab.id}-content`);
            const newTab = document.getElementById(tabName);
            const newTabContent = document.getElementById(`${tabName}-content`);

            currentTab.classList.remove('is-active');
            currentTab.classList.remove('has-text-white');
            currentContent.classList.add('is-hidden');

            newTab.classList.add('is-active');
            newTab.classList.add('has-text-white');
            newTabContent.classList.remove('is-hidden');
        })
    })
});