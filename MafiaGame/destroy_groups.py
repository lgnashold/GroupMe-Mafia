from AUTHTOKEN import AUTH
import groupme_services as gs

def destroy_all_groups(auth_token):
    # Deletes all the groups that a user owns
    page = 1
    group_page = ['not empty']
    while len(group_page) != 0:
        group_page = gs.get_active_groups(auth_token, page)
        print(group_page)
        print("\nAre you sure you want to destroy the following groups? (y/n)")
        print(", ".join([group['name'] for group in group_page]))
        if input('').startswith("y"):
            for group in group_page:
                gs.destroy_group(auth_token, group['id'])
        page += 1

if __name__ == '__main__':
    destroy_all_groups(AUTH)

