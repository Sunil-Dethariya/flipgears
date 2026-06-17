let currentStep = 0;
const steps = document.querySelectorAll('.form-step');
const stepIndicators = document.querySelectorAll('.step');

function showStep(n){
    steps.forEach(s=>s.classList.remove('active'));
    steps[n].classList.add('active');

    stepIndicators.forEach((s,i)=>{
        s.classList.remove('active','completed');
        if(i < n) s.classList.add('completed');
        if(i === n) s.classList.add('active');
    });
}

function nextStep(){
    if(currentStep < steps.length-1){
        currentStep++;
        showStep(currentStep);
    }
}
function prevStep(){
    if(currentStep > 0){
        currentStep--;
        showStep(currentStep);
    }
}



