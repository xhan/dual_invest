<!-- NavBar.vue -->
<template>
    <nav>
        <ul>
            <li>
                <RouterLink to="/btc/sc">
                    BTC 高卖</RouterLink>
            </li>
            <li>
                <RouterLink to="/btc/sp">
                    BTC 低买</RouterLink>
            </li>
            <li>
                <RouterLink to="/eth/sc">
                    ETH 高卖</RouterLink>
            </li>
            <li>
                <RouterLink to="/eth/sp">
                    ETH 低买</RouterLink>
            </li>

        </ul>

    </nav>
</template>

<script>
export default {
    name: 'NavBar',
};
</script>

<style scoped>
nav {
    background-color: #333;
    padding: 1rem;
}

ul {
    list-style-type: none;
    padding: 0;
    display: flex;
    gap: 1rem;
}

li {
    color: white;
}

router-link {
    color: white;
    text-decoration: none;
}

router-link-active {
    font-weight: bold;
}
</style>