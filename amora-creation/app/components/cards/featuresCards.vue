<template>
    <div class="features-cards">
        <div class="cards-header">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
            </button>
        </div>

        <div class="cards-footer">
            <h3>Clarity</h3>
            <p>
                Information is organized so you always
                clearly know whats matters.
            </p>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>

.features-cards {
    background: #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    max-width: 300px;
    min-height: 300px;
    padding: 0.5rem;
    border-radius: 1.5rem;
    transition: all 0.5s ease-in-out;
    cursor: pointer;
}

.features-cards:hover {
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    transform: translateY(-5px);
    transition: all 0.3s ease-in-out;
}

.cards-header{
    padding: 0.5rem;
}

.features-cards button {
    background: #222222;
    padding: 1rem;
    border-radius: 1rem;
    color:#fff;
    font-size: 1.5rem;
}

.cards-footer h3{
    font-size: 1.5rem;
    font-weight: 600;
}

.cards-footer p {
    font-size: 1rem;
    font-weight: 400;
    color:#888888
}
</style>