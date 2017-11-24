<template xmlns="http://www.w3.org/1999/html">
    <div>
        <div class="workticket">
            <h3 class="post-title">{{ticketData.title}}</h3>
            <p class="datetime">创建时间：{{ticketData.create_time}}</p>
            <p class="create_user">创建人：{{ticketData.create_user}}</p>
            <p class="action_user">当前处理人人：{{ticketData.action_user}}</p>
            <div class="content">详细内容：{{ticketData.content}}</div>
        </div>
        <div class="ticketcomment" v-for="item in commentData" :key="item.id">
            <p class="datetime">回复时间：{{item.create_time}}</p>
            <p class="create_user">回复人：{{item.create_user}}</p>
            <div class="content">回复内容：{{item.content}}</div>
        </div>
    </div>
</template>
<script>
    import {getWorkticket, putWorkticket, getTicketcomment, postTicketcomment} from 'api/workticket'

    export default {
        components: {},

        data() {
            return {
                ticketData: {},
                ticket__title: '',
                commentData: {}
            };
        },

        created() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                const ticket_id = 1;
                const ticket_parms = null;
                getWorkticket(ticket_id, ticket_parms).then(response => {
                    this.ticketData = response.data;
                });
                const comment_parms = {
                    ticket__id: 1
                };
                getTicketcomment(comment_parms).then(response => {
                    this.commentData = response.data.results;
                })
            },
        }
    }
</script>

<style lang='scss'>

</style>