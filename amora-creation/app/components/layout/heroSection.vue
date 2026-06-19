<template>
    <section class="main-layout">
        <div class="pic-background">
            <div class="overlay">
                <h1>Nouvelle collection</h1>
                <p>Découvrez nos dernières créations</p>
                <shopButton />
            </div>
            <scrollBar/>
        </div>
    </section>
</template>

<script>
import shopButton from '../buttons/shopButton.vue';
import scrollBar from '../tools/scrollBar.vue';
export default {
    components: {
        shopButton,
        scrollBar
    }

}
</script>

<style scoped>

.pic-background{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    background-image: url('https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.overlay{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.overlay h1{
    font-size: 3rem;
    color: #fff;
    font-weight: bold;
    margin-bottom: 1rem;
    text-align: center;
}

.overlay p{
    font-size: 1.5rem;
    color: #fff;
    margin-bottom: 1rem;
}
</style>