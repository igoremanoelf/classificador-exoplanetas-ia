document.addEventListener('DOMContentLoaded', () => {
    // --- VERIFICAÇÃO INICIAL ---
    if (typeof THREE === 'undefined') {
        console.error("Three.js não foi carregado! Verifique a conexão com a internet ou os links no HTML.");
        return;
    }

    // --- VARIÁVEIS GLOBAIS ---
    let scene, camera, renderer, star, planet, controls;
    let planetData = { object: null };

    // --- ELEMENTOS DO DOM ---
    const form = document.getElementById('prediction-form');
    const predictButton = document.getElementById('predict-button');
    const resultContainer = document.getElementById('result-container');
    const sceneContainer = document.getElementById('scene-container');
    const predictionClassText = document.getElementById('prediction-class-text');

    // --- FUNÇÕES 3D ---
    function init3DScene() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, sceneContainer.clientWidth / sceneContainer.clientHeight, 0.1, 1000);
        camera.position.z = 10;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(sceneContainer.clientWidth, sceneContainer.clientHeight);
        sceneContainer.appendChild(renderer.domElement);
        
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1.5, 100);
        scene.add(pointLight);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        const starGeometry = new THREE.SphereGeometry(2, 32, 32);
        const starMaterial = new THREE.MeshBasicMaterial({ color: 0xffddaa, emissive: 0xffddaa, emissiveIntensity: 1 });
        star = new THREE.Mesh(starGeometry, starMaterial);
        scene.add(star);
        
        animate();
    }

    function animate() {
        requestAnimationFrame(animate);
        if (planetData.object) {
            const time = Date.now() * 0.0005 * (1 / (planetData.period || 10));
            planetData.object.position.x = Math.cos(time) * planetData.distance;
            planetData.object.position.z = Math.sin(time) * planetData.distance;
        }
        controls.update();
        renderer.render(scene, camera);
    }

    // --- LÓGICA DO FORMULÁRIO ---
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        predictButton.textContent = 'Classificando...';
        predictButton.disabled = true;

        const features = {
            koi_fpflag_nt: parseFloat(document.getElementById('koi_fpflag_nt').value),
            koi_fpflag_ss: parseFloat(document.getElementById('koi_fpflag_ss').value),
            koi_fpflag_co: parseFloat(document.getElementById('koi_fpflag_co').value),
            koi_fpflag_ec: parseFloat(document.getElementById('koi_fpflag_ec').value),
            koi_period: parseFloat(document.getElementById('koi_period').value),
            koi_duration: parseFloat(document.getElementById('koi_duration').value),
            koi_depth: parseFloat(document.getElementById('koi_depth').value),
            koi_prad: parseFloat(document.getElementById('koi_prad').value),
            koi_teq: parseFloat(document.getElementById('koi_teq').value),
            koi_model_snr: parseFloat(document.getElementById('koi_model_snr').value),
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(features)
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const data = await response.json();
            displayResult(data, features);
        } catch (error) {
            displayError(error.message);
        } finally {
            predictButton.textContent = 'Classificar';
            predictButton.disabled = false;
        }
    });

    function displayResult(data, features) {
        const { predicted_class } = data;
        predictionClassText.textContent = predicted_class;
        predictionClassText.className = predicted_class.replace(' ', '.');
        
        if (planetData.object) scene.remove(planetData.object);
        
        let planetColor, planetScale = Math.max(0.2, (features.koi_prad || 1) * 0.2); // Escala baseada no raio
        switch (predicted_class) {
            case 'CONFIRMED': planetColor = 0x6699ff; break;
            case 'CANDIDATE': planetColor = 0xffa500; break;
            case 'FALSE POSITIVE': planetColor = 0xff4444; break;
            default: planetColor = 0x888888;
        }
        
        const planetGeometry = new THREE.SphereGeometry(planetScale, 32, 32);
        const planetMaterial = new THREE.MeshStandardMaterial({ color: planetColor });
        planet = new THREE.Mesh(planetGeometry, planetMaterial);
        
        planetData = {
            object: planet,
            distance: 4 + planetScale, // Ajusta a distância para não colidir com a estrela
            period: features.koi_period
        };
        scene.add(planet);
        resultContainer.classList.remove('hidden');
    }

    function displayError(message) {
        predictionClassText.textContent = `Erro: ${message}`;
        predictionClassText.className = 'FALSE.POSITIVE';
        if (planetData.object) {
            scene.remove(planetData.object);
            planetData.object = null;
        }
        resultContainer.classList.remove('hidden');
    }
    
    // Inicia a aplicação
    init3DScene();
});